from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt
import pickle
from IPython import display


from .useful import ts as src
from .useful import iterators

from .models import lstm as models
from . import generate_residuals
from . import stastics

class AnomalyDetection():
    """        
    Pipeline Time Series Anomaly Detection based on 
    SOTA deep learning forecasting algorithms.
    
    Данный пайплайн избавит вас от проблем написания кода для: \n
    1) формирование выборок для подачи в sequence модели \n
    2) обучения моделей \n
    3) поиска аномалий в невязках \n
    
    Данный пайплайн позволяет: \n
    1) пронгозировать временные ряды, в том числе многомерные. \n
    2) вычислять невязку между прогнозом и настоящими значениями \n
    3) анализировать невязку, и возращать разметку аномалиями \n
    
    Parameters
    ----------
    preproc : object, default = sklearn.preprocessing.MinMaxScaler()
        Объект предобратки значений временного ряда.
        Требования к классу по методами атрибутам одинаковы с default.
    
    generate_res_func : func, default = generate_residuals.abs
        Функция генерация невязки. На вход y_pred, y_true. В default это
        абсолютная разница значений. Требования к функциям описаны в 
        generate_residuals.py. 
        
    res_analys_alg : object, default=stastics.Hotelling().
        Объект поиска аномалий в остатках. В default это
        статистика Хоттелинга.Требования к классам описаны в 
        generate_residuals.py. 
        
    
    Attributes
    ----------
    
    
    Return 
    ----------
    object : object Объект этого класса DL_AD

    References
    ----------
    
    Links to the papers 

    Examples
    --------
    https://github.com/waico/tsad/tree/main/examples 
    """

    def _get_Train_Test_sets(self, dfs, len_seq,
                             points_ahead,
                             gap,
                             shag,
                             intersection,
                             test_size,
                             train_size,
                             random_state,
                             shuffle,
                             stratify,
                             ):
        """
        Вспомогательная функция, избавляющая от дубляжа
        """

        if (type(dfs) == pd.core.series.Series) | (type(dfs) == pd.core.frame.DataFrame):
            df = dfs.copy() if type(dfs) == pd.core.frame.DataFrame else pd.DataFrame(dfs)
            self.columns = df.columns
            self.index = df.index
            if self._init_preproc:
                new_df = pd.DataFrame(self.preproc.fit_transform(df), index=df.index, columns=df.columns)
                self._init_preproc = False
            else:
                new_df = pd.DataFrame(self.preproc.transform(df), index=df.index, columns=df.columns)
            assert len_seq + points_ahead + gap - 1 <= len(df)
            X_train, X_test, y_train, y_test = src.ts_train_test_split(df=new_df,
                                                                       len_seq=len_seq,
                                                                       points_ahead=points_ahead,
                                                                       gap=gap,
                                                                       shag=shag,
                                                                       intersection=intersection,
                                                                       test_size=test_size,
                                                                       train_size=train_size,
                                                                       random_state=random_state,
                                                                       shuffle=False,
                                                                       # потому что потом нужно в основном итераторе
                                                                       stratify=stratify)

        elif type(dfs) == type(list()):
            # уже все pd.DataFrame
            _df = pd.concat(dfs, ignore_index=True)
            if self._init_preproc:
                self.preproc.fit(_df)
                self._init_preproc = False
            self.columns = _df.columns
            self.index = _df.index

            X_train, X_test, y_train, y_test = [], [], [], []
            _k = 0
            for df in dfs:
                if ((type(df) == pd.core.series.Series) | (type(df) == pd.core.frame.DataFrame)) == False:
                    raise NameError('Type of dfs is unsupported')
                if not (len_seq + points_ahead + gap + 1 <= len(df)):
                    _k += 1
                    continue

                new_df = pd.DataFrame(self.preproc.transform(df), index=df.index, columns=df.columns)
                _X_train, _X_test, _y_train, _y_test = src.ts_train_test_split(new_df, len_seq,
                                                                               points_ahead=points_ahead,
                                                                               gap=gap,
                                                                               shag=shag,
                                                                               intersection=intersection,
                                                                               test_size=test_size,
                                                                               train_size=train_size,
                                                                               random_state=random_state,
                                                                               shuffle=False,
                                                                               stratify=stratify)
                X_train += _X_train
                X_test += _X_test
                y_train += _y_train
                y_test += _y_test

            print(
                f'Пропущено {_k} датастов, из-за того что saples слишком малов в датасете. (len_seq + points_ahead + gap -1 <= len(df))')

        else:
            raise NameError('Type of dfs is unsupported')

        return X_train, X_test, y_train, y_test

    def _get_anomaly_timestamps(self,
                                dfs,
                                Loader,
                                len_seq,
                                points_ahead,
                                gap,
                                shag,
                                intersection,
                                test_size,
                                random_state,
                                shuffle,
                                stratify,
                                device,
                                point_ahead_for_residuals=0):
        """
        Вспомогательная функция для  генерации всего
        """
        X, _, y_true, _ = self._get_Train_Test_sets(dfs=dfs,
                                                    len_seq=len_seq,
                                                    points_ahead=points_ahead,
                                                    # 1 это default, так с остатками лучше не шутить до сих пор
                                                    gap=gap,
                                                    shag=shag,
                                                    intersection=intersection,
                                                    test_size=test_size,
                                                    train_size=None,
                                                    random_state=random_state,
                                                    shuffle=shuffle,
                                                    stratify=stratify)

        all_data_iterator = Loader(X, y_true, self.batch_size, shuffle=False)
        y_pred = self.model.run_epoch(all_data_iterator, None, None, phase='forecast', points_ahead=points_ahead,
                                      device=device)
        residuals = self.generate_res_func(y_pred, np.array(y_true))
        point_ahead_for_residuals = 0  # мы иногда прогнозим на 10 точек вперед, ну интересует все равно на одну точку впреред
        res_indices = [y_true[i].index[point_ahead_for_residuals] for i in range(len(y_true))]
        df_residuals = pd.DataFrame(residuals[:, point_ahead_for_residuals, :], columns=self.columns,
                                    index=res_indices).sort_index()
        return df_residuals

    # -----------------------------------------------------------------------------------------
    #     Формирование сутевой части класса
    # -----------------------------------------------------------------------------------------

    def __init__(self,
                 preproc=None,
                 generate_res_func=None,
                 res_analys_alg=None,

                 ):

        self.preproc = MinMaxScaler() if preproc is None else preproc
        self.generate_res_func = generate_residuals.abs if generate_res_func is None else generate_res_func
        self.res_analys_alg = stastics.Hotelling() if res_analys_alg is None else res_analys_alg

    def fit(self,
            dfs,
            targets=None, # for RUL task. 
            model=None,
            encod_decode_model=False,
            # ужас, нужно это править, особенность encod_decode модели. Попытаться вообще еубрать эту переменную
            criterion=None,
            optimiser=None,
            batch_size=64,
            len_seq=10,
            points_ahead=5,
            n_epochs=100,
            gap=0,
            shag=1,
            intersection=True,
            test_size=0.2,
            train_size=None,
            random_state=None,
            shuffle=False,
            show_progress=True,
            show_figures=True,
            best_model_file='./best_model.pt',
            stratify=None,
            Loader=None,

            ):

        """
        Обучение модели как для задачи прогнозирования так и для задачи anomaly
        detection на имеющихся данных. fit = fit_predict_anmaloy 
        
        Parameters
        ----------
        dfs : {{df*,ts*}, list of {df*,ts*}}
            df*,ts* are pd.core.series.Seriesor or pd.core.frame.DataFrame data type.
            Исходные данные. Данные не долнжны содержать np.nan вовсе, иметь постоянную 
            и одинковую частоту of df.index и при этом не иметь пропусков. Проблему с 
            пропуском решают дробление одно df на list of df.             
        
        model : object of torch.nn.Module class, default=models.SimpleLSTM()
            Используемая модель нейронной сети. 
        
        criterion : object of torch.nn class, default=nn.MSELoss()
            Критерий подсчета ошибки для оптмизации. 
        
        optimiser : tuple = (torch.optim class ,default = torch.optim.Adam,
            dict  (dict of arguments without params models) , default=default)
            Example of optimiser : optimiser=(torch.optim.Adam,{'lr':0.001})
            Метод оптимизации нейронной сети и его параметры, указанные в 
            документации к torch.
            
        batch_size :  int, default=64
            Размер батча (Число сэмплов по которым усредняется градиент)
        
        len_seq : int, default=10
            Размер окна (количество последовательных точек ряда), на котором
            модель реально работает. По сути аналог порядка в авторегрессии. 
        
        points_ahead : int, default=5
            Горизонт прогнозирования. 
        
        n_epochs :  int, default=100 
            Количество эпох.
        
        >>> train_test_split vars
        
            gap :  int, default=0
                Сколько точек между трейном и тестом. Условно говоря,
                если крайняя точка train а это t, то первая точка теста t + gap +1.
                Параметр создан, чтобы можно было прогнозировать одну точку через большой 
                дополнительный интервал времени. 
            
            shag :  int, default=1.
                Шаг генерации выборки. Если первая точка была t у 1-ого сэмпла трейна,
                то у 2-ого сэмла трейна она будет t + shag, если intersection=True, иначе 
                тоже самое но без пересечений значений ряда. 
        
            intersection :  bool, default=True
                Наличие значений ряда (одного момента времени) в различных сэмплах выборки. 
            
            test_size : float or int, default=None
                If float, should be between 0.0 and 1.0 and represent the proportion
                of the dataset to include in the test split. If int, represents the
                absolute number of test samples. If None, the value is set to the
                complement of the train size. If ``train_size`` is also None, it will
                be set to 0.25. *
                *https://github.com/scikit-learn/scikit-learn/blob/95119c13a/sklearn/model_selection/_split.py#L2076 
                Может быть 0, тогда вернет значения X,y
            
            train_size : float or int, default=None
                If float, should be between 0.0 and 1.0 and represent the
                proportion of the dataset to include in the train split. If
                int, represents the absolute number of train samples. If None,
                the value is automatically set to the complement of the test size. *
                *https://github.com/scikit-learn/scikit-learn/blob/95119c13a/sklearn/model_selection/_split.py#L2076
            
            random_state : int, RandomState instance or None, default=None
                Controls the shuffling applied to the data before applying the split.
                Pass an int for reproducible output across multiple function calls.
                See :term:`Glossary <random_state>`.*
                *https://github.com/scikit-learn/scikit-learn/blob/95119c13a/sklearn/model_selection/_split.py#L2076
                
            
            shuffle : bool, default=True
                Whether or not to shuffle the data before splitting. If shuffle=False
                then stratify must be None. *
            
            show_progress : bool, default=True
                Показывать или нет прогресс обучения с детализацией по эпохам. 

            
            show_figures : bool, default=True
                Показывать или нет результаты решения задачии anomaly detection 
                и кривую трейна и валидации по эпохам. 
            
            
            best_model_file : string, './best_model.pt'
                Путь до файла, где будет хранится лучшие веса модели
            
            Loader : class, default=ufesul.iterators.Loader.
                Тип загрузчика, которую будет использовать как итератор в будущем, 
                благодаря которому, есть возможность бить на бачи.
        
        Attributes
        ----------

        Return 
        ----------
        list of pd.datetime anomalies on initial dataset
        """
        self._init_preproc = True  # это кастыль для _get_Train_Test_sets
        self.points_ahead = points_ahead
        self.len_seq = len_seq
        self.batch_size = batch_size
        dfs = dfs.copy()
        self.best_model_file = best_model_file
        self.encod_decode_model = encod_decode_model
        if show_progress:
            show_progress_text = ""

        # -----------------------------------------------------------------------------------------
        #     Формирование train_iterator и val_iteraror
        # -----------------------------------------------------------------------------------------
        if Loader is None:
            Loader = iterators.Loader

        X_train, X_test, y_train, y_test = self._get_Train_Test_sets(dfs=dfs,
                                                                     len_seq=len_seq,
                                                                     points_ahead=points_ahead,
                                                                     gap=gap,
                                                                     shag=shag,
                                                                     intersection=intersection,
                                                                     test_size=test_size,
                                                                     train_size=train_size,
                                                                     random_state=random_state,
                                                                     shuffle=shuffle,
                                                                     stratify=stratify)

        train_iterator = Loader(X_train, y_train, batch_size, shuffle=shuffle)
        val_iterator = Loader(X_test, y_test, batch_size, shuffle=shuffle)

        # -----------------------------------------------------------------------------------------
        #     Обучение моделей
        # -----------------------------------------------------------------------------------------

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if criterion is None:
            criterion = nn.MSELoss()

        if model is None:
            model = models.SimpleLSTM(len(self.columns), len(self.columns), seed=random_state)
        self.model = model

        if optimiser is None:
            optimiser = torch.optim.Adam
            optimiser = optimiser(self.model.parameters())
        else:
            args = optimiser[1]
            args['params'] = self.model.parameters()
            optimiser = optimiser[0](**args)

        history_train = []
        history_val = []
        best_val_loss = float('+inf')
        for epoch in range(n_epochs):
            train_loss = self.model.run_epoch(train_iterator, optimiser, criterion, phase='train',
                                              points_ahead=points_ahead, encod_decode_model=self.encod_decode_model,
                                              device=device)  # , writer=writer)
            val_loss = self.model.run_epoch(val_iterator, None, criterion, phase='val', points_ahead=points_ahead,
                                            encod_decode_model=self.encod_decode_model,
                                            device=device)  # , writer=writer)

            history_train.append(train_loss)
            history_val.append(val_loss)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), self.best_model_file)

            if show_figures:
                display.clear_output(wait=True)
                plt.figure()
                plt.plot(history_train, label='Train')
                plt.plot(history_val, label='Val')
                plt.xlabel('Epoch')
                plt.ylabel('MSE')
                plt.legend()
                plt.show()

            if show_progress:
                show_progress_text = f'Epoch: {epoch + 1:02} \n' + \
                                     f'\tTrain Loss: {train_loss:.3f} \n' + \
                                     f'\t Val. Loss: {val_loss:.3f} \n\n' +  \
                                     show_progress_text
                print(show_progress_text)




        self.model.load_state_dict(torch.load(self.best_model_file))

        if show_progress:
            print("After choosing the best model:")
            try:
                test_iterator = Loader(X_test, y_test, len(X_test), shuffle=False)
                test_loss = self.model.run_epoch(test_iterator, None, criterion, phase='val',
                                                 encod_decode_model=self.encod_decode_model, device=device)
                print(f'Test Loss: {test_loss:.3f}')
            except:
                print('Весь X_test не помещается в память, тестим усреднением по батчам')
                test_iterator = Loader(X_test, y_test, batch_size, shuffle=False)
                test_loss = []
                for epoch in range(n_epochs):
                    test_loss.append(self.model.run_epoch(test_iterator, None, criterion, phase='val',
                                                          encod_decode_model=self.encod_decode_model, device=device))
                print(f'Test Loss: {np.mean(test_loss):.3f}')


        # -----------------------------------------------------------------------------------------
        #     Генерация остатков
        # -----------------------------------------------------------------------------------------
        df_residuals = self._get_anomaly_timestamps(dfs=dfs,
                                                    Loader=Loader,
                                                    len_seq=len_seq,
                                                    points_ahead=1,
                                                    gap=gap,
                                                    shag=shag,
                                                    intersection=intersection,
                                                    test_size=0,
                                                    random_state=None,
                                                    shuffle=False,
                                                    stratify=stratify,
                                                    device=device,
                                                    point_ahead_for_residuals=0)
        self.anomaly_timestamps = self.res_analys_alg.fit_predict(df_residuals, show_figure=show_figures)
        self.statistic = self.res_analys_alg.statistic
        self.ucl = self.res_analys_alg.ucl
        self.lcl = self.res_analys_alg.lcl
        return self.anomaly_timestamps

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # накосячил тут с прогнозом на одну точку вперед. Могут быть проблемы если ahead !=1
    def predict_anomaly(self,
                        dfs,
                        Loader=None,
                        gap=0,
                        shag=1,
                        intersection=True,
                        train_size=None,
                        random_state=None,
                        shuffle=False,
                        stratify=None,
                        show_progress=True,
                        show_figures=True
                        ):

        """
        Поиск аномалий в новом наборе данных
        
        Parameters
        ----------
        см self.fit() dockstring
        
        
        Return
        ----------
        anomaly_timestamps : list of df.index.dtype
            Возвращает список временных меток аномалий                
        
        Attributes
        ----------
        
        """
        len_seq = self.len_seq

        if Loader is None:
            Loader = iterators.Loader

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # -----------------------------------------------------------------------------------------
        #     Генерация остатков
        # -----------------------------------------------------------------------------------------
        df_residuals = self._get_anomaly_timestamps(dfs=dfs,
                                                    Loader=Loader,
                                                    len_seq=len_seq,
                                                    points_ahead=1,
                                                    gap=gap,
                                                    shag=shag,
                                                    intersection=intersection,
                                                    test_size=0,
                                                    random_state=None,
                                                    shuffle=False,
                                                    stratify=stratify,
                                                    device=device,
                                                    point_ahead_for_residuals=0)
        self.anomaly_timestamps = self.res_analys_alg.predict(df_residuals, show_figure=show_figures)
        self.statistic = self.res_analys_alg.statistic
        return self.anomaly_timestamps

    def forecast(self, df, points_ahead=None, Loader=None, show_figures=True):
        """
        Прогнозирование временного ряда, в том числе векторного.
        
        Parameters
        ----------
        df : pd.core.series.Series or pd.core.frame.DataFrame data type
            Исходные данные. Данные не долнжны содержать np.nan вовсе, иметь постоянную 
            и одинковую частоту of df.index и при этом не иметь пропусков.         
                
        points_ahead : int, default=5
            Горизонт прогнозирования. 
               
        show_figures : bool, default=True
            Показывать или нет результаты решения задачии anomaly detection 
            и кривую трейна и валидации по эпохам. 
        
        
        Loader : class, default=iterators.Loader.
            Тип загрузчика, которую будет использовать как итератор в будущем, 
            благодаря которому, есть возможность бить на бачи.
        
                
        

        
        Attributes
        ----------
        
        """
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if Loader is None:
            Loader = iterators.Loader

        df = df.copy()
        points_ahead = points_ahead if points_ahead is not None else self.points_ahead
        len_seq = self.len_seq
        batch_size = self.batch_size

        assert (type(df) == pd.core.series.Series) | (type(df) == pd.core.frame.DataFrame)
        df = df.copy() if type(df) == pd.core.frame.DataFrame else pd.DataFrame(df)
        df = df[-len_seq:]
        assert not self._init_preproc
        preproc_values = self.preproc.transform(df)

        iterator = Loader(np.expand_dims(preproc_values, 0), np.expand_dims(preproc_values, 0),
                          # ничего страшного, 'y' все равно не используется
                          batch_size, shuffle=False)

        y_pred = self.model.run_epoch(iterator, None, None, phase='forecast', points_ahead=points_ahead, device=device)[
            0]
        y_pred = self.preproc.inverse_transform(y_pred)

        t_last = np.datetime64(df.index[-1])
        delta_dime = np.timedelta64(df.index[-1] - df.index[-2])
        new_index = pd.to_datetime(t_last + np.arange(1, points_ahead + 1) * delta_dime)
        y_pred = pd.DataFrame(y_pred, index=new_index, columns=df.columns)

        if show_figures:
            pd.concat([df, y_pred])[-3 * points_ahead:].plot()
            plt.axvspan(t_last, y_pred.index[-1], alpha=0.2, color='green', label='forecast')
            plt.xlabel('Datetime')
            plt.ylabel('Value')
            plt.legend()
            plt.show()

        return y_pred

    def save(self, path='./pipeline.pcl'):
        """
        Method for saving pipeline.
        It may be required for example after training.
        CPU.
        
        Parameters
        ----------
            path : str
        Путь до файла, для сохранения пайплайна. 
        Пайлайн сохраняется в формате pickle
        """

        self.model.run_epoch(iterators.Loader(torch.zeros((1, self.len_seq, self.model.in_features), dtype=float),
                                        torch.zeros((1, self.len_seq, self.model.in_features), dtype=float),
                                        batch_size=1),
                             None, None, phase='forecast', points_ahead=1, device=torch.device("cpu"))
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, path='./pipeline.pcl'):
        """
        Method for loading pipeline.
        It may be required for example after training.
        
        Parameters
        ----------
            path : str
        Путь до сохраненного файла пайплайна. 
        Пайлайн должен быть в формате pickle
        """
        with open(path, 'rb') as f:
            pipeline = pickle.load(f)
        self.__dict__.update(pipeline.__dict__)
