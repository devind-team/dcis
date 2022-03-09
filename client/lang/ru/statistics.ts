export default {
  menu: {
    eduPrograms: '@:eduPrograms.name'
  },
  eduProgramsStatistics: {
    name: '@:statistics.menu.eduPrograms',
    filters: {
      directionsFilter: {
        title: 'Фильтр направлений подготовки',
        noFiltrationMessage: 'Все направления подготовки',
        multipleMessage: '{name} и еще {restLength} направлений подготовки |' +
          ' {name} и еще {restLength} направление подготовки |' +
          ' {name} и еще {restLength} направления подготовки'
      },
      yearsFilter: {
        title: 'Фильтр лет',
        noFiltrationMessage: 'Все года',
        multipleMessage: '{name} и еще {restLength} лет | {name} и еще {restLength} год |' +
          ' {name} и еще {restLength} года',
        year: '{year} год'
      },
      eduFormsFilter: {
        title: 'Фильтр форм обучения',
        noFiltrationMessage: 'Все формы обучения',
        multipleMessage: '{name} и еще {restLength} форм обучения | {name} и еще {restLength} форма обучения |' +
          ' {name} и еще {restLength} формы обучения'
      }
    },
    view: {
      'chart-arc': 'Представление в графическом виде',
      table: 'Представление в табличном виде'
    },
    eduPrograms: 'Образовательные программы',
    disciplines: 'Дисциплины',
    labels: {
      description: 'Описание образовательных программ',
      syllabus: 'Учебный план',
      calendar: 'Календарный график учебного процесса',
      users: 'Авторы',
      annotation: 'Аннотации',
      workProgram: 'Рабочие программы',
      methodologicalSupport: 'Методическое обеспечение'
    },
    indicatorLabels: {
      availability: 'Заполнено',
      lack: 'Отсутствует'
    }
  },
  statistics: 'Показатели электронной среды обучения'
}
