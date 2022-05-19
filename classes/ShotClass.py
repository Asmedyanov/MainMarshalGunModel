"""Модель выстрела из пушки. Все величины в СИ"""
from pandas import DataFrame
import numpy as np
import scipy.integrate as spint
import matplotlib.pyplot as plt

R_gas = 8.31
"""Газовая постоянная"""
aem = 1.7e-27
"""Атомная единица массы"""
N_Avagadro = 6.02e23
"""Число Авагадро"""


class Shot:
    def __init__(self, *args, **kwargs):
        self.mCoordinat_mult = None
        """Нормировка координаты"""
        self.mSpeed_mult = None
        """Нормировка скорости"""
        self.mInitial_solution = [0, 0, 1.0, 0]
        """Начальные условия"""
        self.mTime_norm = None
        """Нормированное время"""
        self.mTime = None
        """Реальное время"""
        self.mQ_gun = None
        """Силовой параметр"""
        self.mL_linear = None
        """Погонная индуктивность"""
        self.mOmega_0 = None
        """Собственная частота контура пушки"""
        self.mM_gas = None
        """Масса вещества в клапане"""
        self.mNu_gas = None
        """Количество вещества в клапане"""
        self.mTime_length = None
        """Длительность моделирования"""
        self.mTime_step = None
        """Шаг по времени моделирования"""
        self.mT_gas = None
        """Температура газа"""
        self.mPart = None
        """Масса частицы"""
        self.mP_valve = None
        """Давление в клапане"""
        self.mV_valve = None
        """Объем клапана"""
        self.mGun_length = None
        """Длина пушки"""
        self.mD_out = None
        """Внешний диаметр пушки"""
        self.mD_in = None
        """Внутренний диаметр пушки"""
        self.mL0 = None
        """Индуктивность проводов пушки"""
        self.mU0 = None
        """Начальное напряжение на накопителе"""
        self.mCapacity = None
        """Ёмкость накопителя"""
        try:
            self.init_full(*args, **kwargs)
        except:
            self.init_default()

    def init_full(self, *args, **kwargs):
        """Полная инициализация"""
        self.mCapacity = kwargs['Capacity']
        self.mU0 = kwargs['U0']
        self.mL0 = kwargs['L0']
        self.mD_in = kwargs['D_in']
        self.mD_out = kwargs['D_out']
        self.mGun_length = kwargs['Gun_length']
        self.mV_valve = kwargs['V_valve']
        self.mP_valve = kwargs['P_valve']
        self.mPart = kwargs['Part'] * aem
        self.mT_gas = kwargs['T_gas']
        self.mTime_step = kwargs['Time_step']
        self.mTime_length = kwargs['Time_length']
        self.prepare_data()
        self.find_solution()

    def init_default(self):
        """Инициализация по умолчанию"""
        self.mCapacity = 560.0e-6
        self.mU0 = 2.0e3
        self.mL0 = 270.0e-9
        self.mD_in = 10.0e-3
        self.mD_out = 40.0e-3
        self.mV_valve = 1.0e-6
        self.mP_valve = 1.0e5
        self.mPart = 2.0 * aem
        self.mT_gas = 300.0
        self.mTime_step = 1.0e-7
        self.mTime_length = 100.0e-6
        self.mGun_length = 1.0
        self.prepare_data()
        self.find_solution()

    def prepare_data(self):
        """Подготовка данных к моделированию"""
        self.mNu_gas = self.mP_valve * self.mV_valve / (self.mT_gas * R_gas)
        self.mM_gas = self.mPart * self.mNu_gas * N_Avagadro
        self.mOmega_0 = 1.0 / np.sqrt(self.mL0 * self.mCapacity)
        self.mL_linear = 2.0e-7 * np.log(self.mD_out / self.mD_in)
        self.mQ_gun = np.power(self.mL_linear * self.mCapacity * self.mU0, 2) / (2.0 * self.mM_gas * self.mL0)
        self.mTime = np.arange(0.0, self.mTime_length, self.mTime_step)
        self.mTime_norm = self.mTime * self.mOmega_0
        self.mSpeed_mult = 1.0 / (self.mL_linear * np.sqrt(self.mCapacity / self.mL0))
        self.mCoordinat_mult = self.mL0 / self.mL_linear
        self.mVoltage_mult = self.mU0
        self.mCurrent_mult = self.mCapacity * self.mU0 * self.mOmega_0

    def find_solution(self):
        def WorkEquation(y, t):
            ret0 = self.mQ_gun * (y[3] ** 2)
            ret1 = y[0]
            ret2 = -y[3]
            ret3 = (y[2] - (y[0] * y[3])) / (1.0 + y[1])
            return [ret0, ret1, ret2, ret3]

        Solution = spint.odeint(WorkEquation, self.mInitial_solution, self.mTime_norm)
        Solution_T = Solution.T
        y_ = Solution_T[0]
        y = Solution_T[1]
        f = Solution_T[2]
        f_ = Solution_T[3]
        self.mSpeed = y_ * self.mSpeed_mult / 1.0e3
        self.mCoordinat = y * self.mCoordinat_mult
        self.mVoltage = f * self.mVoltage_mult / 1.0e3
        self.mCurrent = f_ * self.mCurrent_mult / 1.0e3

    def plot(self):
        plt.subplot(4, 1, 1)
        plt.plot(self.mTime * 1.0e6, self.mVoltage)
        plt.xlabel("Время, мкс")
        plt.ylabel("Напряжение, кВ")
        plt.grid()

        plt.subplot(4, 1, 2)
        plt.plot(self.mTime * 1.0e6, self.mCurrent)
        plt.xlabel("Время, мкс")
        plt.ylabel("Ток, кА")
        plt.grid()

        plt.subplot(4, 1, 3)
        plt.plot(self.mTime * 1.0e6, self.mSpeed)
        plt.xlabel("Время, мкс")
        plt.ylabel("Скорость, км/с")
        plt.grid()

        plt.subplot(4, 1, 4)
        plt.plot(self.mTime * 1.0e6, self.mCoordinat)
        plt.xlabel("Время, мкс")
        plt.ylabel("Координата, м")
        plt.grid()

        plt.show()
