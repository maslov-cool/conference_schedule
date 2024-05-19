import datetime

performances = []


class Report:
    def __init__(self, topic, start_time, duration):
        # start_time типа datetime.datetime
        # duration типа datetime.timedelta
        self.topic = topic
        self.start_time = start_time
        self.duration = duration


class Conference:
    def __init__(self, topic, start_time, duration):
        # start_time в формате '11:00 24.05.2024'
        # duration в формате '11:00'
        self.topic = topic
        self.start_time = datetime.datetime(int(start_time.split()[1].split('.')[-1]),
                                            int(start_time.split()[1].split('.')[1]),
                                            int(start_time.split()[1].split('.')[0]),
                                            hour=int(start_time.split()[0].split(':')[0]),
                                            minute=int(start_time.split()[0].split(':')[1]))
        self.duration = datetime.timedelta(hours=int(duration.split(':')[0]), minutes=int(duration.split(':')[1]))

    def add_performance(self, topic, start_time, duration):
        global performances
        # минимальное время перерыва между докладами 10 минут
        start_time = datetime.datetime(int(start_time.split()[1].split('.')[-1]),
                                       int(start_time.split()[1].split('.')[1]),
                                       int(start_time.split()[1].split('.')[0]),
                                       hour=int(start_time.split()[0].split(':')[0]),
                                       minute=int(start_time.split()[0].split(':')[1]))
        duration = datetime.timedelta(hours=int(duration.split(':')[0]), minutes=int(duration.split(':')[1]))
        if not (self.start_time <= start_time and self.start_time + self.duration >= start_time + duration):
            print('Время выступления не помещается в рамки времени конференции, попробуйте изменить его')
        elif not all(True if i.start_time > start_time + duration or i.start_time + i.duration < start_time
                     else False for i in performances):
            print('Доклады не должны перекрываться по времени')
        elif not all(True if min(abs((i.start_time - (start_time + duration)).total_seconds() / 60),
                                 abs((start_time - (i.start_time + duration)).total_seconds() / 60)) >= 5
                     else False for i in performances):
            print('Минимальное время перерыва между докладами 10 минут !!!')
        else:
            performances.append(Report(topic, start_time, duration))
            performance = sorted(performances, key=lambda x: x.start_time)
            print('Выступление удачно добавлено!')

    def sum_time_reports(self):
        sum_time = datetime.timedelta(hours=0, minutes=0)
        for i in performances:
            sum_time += i.duration
        print(f'Суммарное время: {int(sum_time.total_seconds() / 3600)} часов '
              f'{int(sum_time.total_seconds() / 60) - int(sum_time.total_seconds() / 3600) * 60} '
              f'минут')

    def longest_break(self):
        # в минутах
        m = int(min((performances[i + 1].start_time -
                     (performances[i].start_time + performances[i].duration)).total_seconds() // 60
                    for i in range(len(performances) - 1)))
        print(f'Самый продолжительный перерыв длится {m}  минут')

    def list_performances(self):
        print(f'План конференции {self.topic}')
        for i in performances:
            print(f'{i.start_time.hour}:{(i.start_time).minute} - {(i.start_time + i.duration).hour}:'
                  f'{(i.start_time + i.duration).minute} : доклад {i.topic}')


# создадим конференцию 'Python', 19 мая 2024 12:00, длительность 5 часов:
# Первое выступление: 'Библиотека Numpy', 19 мая 2024 12:10, длительность 2 часа:
# Второе выступление: 'Библиотека Twiner', 19 мая 2024 14:20, длительность 2 часа 30 минут:
conference = Conference('Python', '12:00 24.05.2024', '5:00')

conference.add_performance('Библиотека Numpy', '12:10 24.05.2023', '2:00')
conference.add_performance('Библиотека Numpy', '12:10 24.05.2024', '2:00')

conference.add_performance('Библиотека Twiner', '13:10 24.05.2024', '2:00')
conference.add_performance('Библиотека Twiner', '14:12 24.05.2024', '2:00')
conference.add_performance('Библиотека Twiner', '14:20 24.05.2024', '2:00')

conference.sum_time_reports()
conference.longest_break()

conference.list_performances()
