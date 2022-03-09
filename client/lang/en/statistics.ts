export default {
  menu: {
    eduPrograms: '@:eduPrograms.name'
  },
  eduProgramsStatistics: {
    name: '@:statistics.menu.eduPrograms',
    filters: {
      directionsFilter: {
        title: 'Direction filter',
        noFiltrationMessage: 'All direction',
        multipleMessage: '{name} and {restLength} more directions | {name} and {restLength} more directions |' +
          ' {name} and {restLength} more directions'
      },
      yearsFilter: {
        title: 'Year filter',
        noFiltrationMessage: 'All years',
        multipleMessage: '{name} and {restLength} more years | {name} and {restLength} more years |' +
          ' {name} and {restLength} more years',
        year: '{year} year'
      },
      eduFormsFilter: {
        title: 'Form of study filter',
        noFiltrationMessage: 'All forms of study',
        multipleMessage: '{name} and {restLength} forms of study | {name} and {restLength} forms of study |' +
          ' {name} and {restLength} forms of study'
      }
    },
    view: {
      'chart-arc': 'Graph view',
      table: 'Table view'
    },
    eduPrograms: 'Educational programs',
    disciplines: 'Disciplines',
    labels: {
      description: 'Description of educational programs',
      syllabus: 'Syllabus',
      calendar: 'Academic calendar',
      users: 'Authors',
      annotation: 'Annotations',
      workProgram: 'Work programs',
      methodologicalSupport: 'Methodological support'
    },
    indicatorLabels: {
      availability: 'Available',
      lack: 'Unavailable'
    }
  },
  statistics: '@:statistics.dashboard'
}
