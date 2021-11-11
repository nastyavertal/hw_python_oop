from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM = 1000
    H_IN_M = 60
    LEN_STEP = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_FOR_RUN = 18
    COEFF_FOR_RUN_2 = 20

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_FOR_RUN * self.get_mean_speed()
                    - self.COEFF_FOR_RUN_2)
                    * self.weight / self.M_IN_KM * self.duration * self.H_IN_M)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_FOR_WALK = 0.035
    COEFF_FOR_WALK_2 = 0.029

    height: int

    def get_spent_calories(self) -> float:
        calories = ((self.COEFF_FOR_WALK * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * self.COEFF_FOR_WALK_2 * self.weight)
                    * self.duration * self.H_IN_M)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    count_pool: float
    length_pool: float

    LEN_STEP = 1.38
    FIRST_COEFF_FOR_SWIM = 1.1
    SECOND_COEFF_FOR_SWIM = 2

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.FIRST_COEFF_FOR_SWIM)
                    * self.SECOND_COEFF_FOR_SWIM * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking}
    if workout_type not in workouts:
        raise KeyError('неверный тип тренировки')
    elif len(data) > 5:
        raise TypeError('передано неверное количество аргументов')
    else:
        return workouts[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
