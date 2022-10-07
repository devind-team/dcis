export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  Date: any;
  DateTime: any;
  JSONString: any;
  Upload: any;
};

/** Токен. */
export type AccessTokenType = {
  __typename?: 'AccessTokenType';
  application?: Maybe<ApplicationType>;
  created: Scalars['DateTime'];
  expires: Scalars['DateTime'];
  id: Scalars['ID'];
  scope: Scalars['String'];
  session?: Maybe<SessionType>;
  token: Scalars['String'];
  updated: Scalars['DateTime'];
  user?: Maybe<UserType>;
};

/**
 * Типы измнения связей между записями в базе данных
 * - ADD - Добавление
 * - DELETE - Удаление
 */
export type ActionRelationShip =
  | 'ADD'
  | 'DELETE';

export type ActiveBudgetClassificationCodeFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type ActiveBudgetClassificationFilterInputType = {
  /** `And` field */
  and?: InputMaybe<Array<InputMaybe<ActiveBudgetClassificationFilterInputType>>>;
  /** `Code` field */
  code?: InputMaybe<ActiveBudgetClassificationCodeFilterInputType>;
  /** `Id` field */
  id?: InputMaybe<ActiveBudgetClassificationIdFilterInputType>;
  /** `Not` field */
  not?: InputMaybe<ActiveBudgetClassificationFilterInputType>;
  /** `Or` field */
  or?: InputMaybe<Array<InputMaybe<ActiveBudgetClassificationFilterInputType>>>;
};

export type ActiveBudgetClassificationIdFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['ID']>;
  /** `In` lookup */
  in?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

/** Информация активности пользователей и времени ответа браузеров. */
export type ActiveStatisticsType = {
  __typename?: 'ActiveStatisticsType';
  /** Запросы */
  queries: Array<Maybe<DateStatisticsType>>;
  /** Время ответа сервера */
  times: Array<Maybe<DateStatisticsType>>;
};

export type AddAttributeMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  default?: InputMaybe<Scalars['String']>;
  id?: InputMaybe<Scalars['ID']>;
  /** Ключ */
  key: Scalars['String'];
  /** Тип атрибута */
  kind: Scalars['String'];
  /** Можно ли изменять */
  mutable?: InputMaybe<Scalars['Boolean']>;
  /** Наименование атрибута */
  name: Scalars['String'];
  parent?: InputMaybe<Scalars['ID']>;
  period: Scalars['ID'];
  /** Подсказка */
  placeholder: Scalars['String'];
  position?: InputMaybe<Scalars['Int']>;
};

export type AddAttributeMutationPayload = {
  __typename?: 'AddAttributeMutationPayload';
  attribute?: Maybe<AttributeType>;
  clientMutationId?: Maybe<Scalars['String']>;
  errors?: Maybe<Array<Maybe<ErrorType>>>;
};

export type AddBudgetClassificationMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Code */
  code: Scalars['String'];
  /** Name */
  name: Scalars['String'];
};

/** Мутация для добавления КБК в словарь. */
export type AddBudgetClassificationMutationPayload = {
  __typename?: 'AddBudgetClassificationMutationPayload';
  /** Добавленная КБК */
  budgetClassification?: Maybe<BudgetClassificationType>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddCategoryMutationInput = {
  /** Аватар */
  avatar?: InputMaybe<Scalars['Upload']>;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор родительской категории */
  parentId?: InputMaybe<Scalars['ID']>;
  /** Название категории */
  text: Scalars['String'];
};

/** Мутация для добавления категории */
export type AddCategoryMutationPayload = {
  __typename?: 'AddCategoryMutationPayload';
  /** Добавленная котегория */
  category?: Maybe<CategoryType>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddChildRowDimensionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор документа */
  documentId: Scalars['ID'];
  /** Индекс вставки в плоскую структуру */
  globalIndex: Scalars['Int'];
  /** Вспомогательные индексы в плоской структуре */
  globalIndices: Array<GlobalIndicesInputType>;
  /** Индекс вставки */
  index: Scalars['Int'];
  /** Идентификатор родительской строки */
  parentId: Scalars['ID'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
};

/** Добавление дочерней строки. */
export type AddChildRowDimensionMutationPayload = {
  __typename?: 'AddChildRowDimensionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленная строка */
  rowDimension: RowDimensionType;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddDivisionsFromFileMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Файл в формате xlsx, csv */
  file?: InputMaybe<Scalars['Upload']>;
  /** Идентификатор периода */
  periodId: Scalars['ID'];
};

/** Мутация для добавления дивизионов из файла. */
export type AddDivisionsFromFileMutationPayload = {
  __typename?: 'AddDivisionsFromFileMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Новые дивизионы */
  divisions: Array<Maybe<DivisionModelType>>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Не найденные дивизионы */
  missingDivisions: Array<Maybe<Scalars['Int']>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddDivisionsFromPeriodMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор периода отдачи */
  periodFromId: Scalars['ID'];
  /** Идентификатор периода */
  periodId: Scalars['ID'];
};

/** Мутация для добавления дивизионов из других периодов. */
export type AddDivisionsFromPeriodMutationPayload = {
  __typename?: 'AddDivisionsFromPeriodMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Новые дивизионы */
  divisions: Array<Maybe<DivisionModelType>>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddDivisionsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификаторы дивизионов */
  divisionIds?: InputMaybe<Array<Scalars['ID']>>;
  /** Идентификатор периода */
  periodId: Scalars['ID'];
};

/** Мутация на добавление дивизионов в период. */
export type AddDivisionsMutationPayload = {
  __typename?: 'AddDivisionsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Новые дивизионы */
  divisions: Array<Maybe<DivisionModelType>>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddDocumentDataMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Комментарий */
  comment?: InputMaybe<Scalars['String']>;
  /** Файл с данными */
  file: Scalars['Upload'];
  /** Идентификатор периода */
  periodId: Scalars['ID'];
  /** Статус */
  statusId: Scalars['ID'];
};

/** Загрузка данных из файла. */
export type AddDocumentDataMutationPayload = {
  __typename?: 'AddDocumentDataMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Список созданных документов */
  documents?: Maybe<Array<Maybe<DocumentType>>>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddDocumentMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Комментарий */
  comment: Scalars['String'];
  /** Идентификатор дивизиона */
  divisionId?: InputMaybe<Scalars['ID']>;
  /** Идентификатор документа, от которого создавать копию */
  documentId?: InputMaybe<Scalars['ID']>;
  /** Идентификатор периода */
  periodId: Scalars['ID'];
  /** Идентификатор начального статуса документа */
  statusId: Scalars['ID'];
};

/** Добавление документа. */
export type AddDocumentMutationPayload = {
  __typename?: 'AddDocumentMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Созданный документ */
  document?: Maybe<DocumentType>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddDocumentStatusMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Комментарий */
  comment?: InputMaybe<Scalars['String']>;
  /** Документ */
  documentId: Scalars['ID'];
  /** Статус */
  statusId: Scalars['ID'];
};

/** Добавление статуса документа. */
export type AddDocumentStatusMutationPayload = {
  __typename?: 'AddDocumentStatusMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Статус документа */
  documentStatus?: Maybe<DocumentStatusType>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddFileMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемые файлы */
  files: Array<Scalars['Upload']>;
  /** Идентификатор пользователя */
  userId?: InputMaybe<Scalars['ID']>;
};

/** Мутация для загрузки файлов */
export type AddFileMutationPayload = {
  __typename?: 'AddFileMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Загруженные файлы */
  files: Array<Maybe<FileType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddGroupMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Название группы */
  name: Scalars['String'];
  permissionFrom?: InputMaybe<Scalars['Int']>;
};

/** Мутация для добавления группы. */
export type AddGroupMutationPayload = {
  __typename?: 'AddGroupMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленная группа */
  group?: Maybe<GroupType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddPageMutationInput = {
  /** Аватар */
  avatar?: InputMaybe<Scalars['Upload']>;
  /** Категория страницы */
  categoryId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Скрываем ли страницу */
  hide?: InputMaybe<Scalars['Boolean']>;
  /** Тип страницы */
  kindId?: InputMaybe<Scalars['Int']>;
  /** Показывать параллакс или нет */
  parallax?: InputMaybe<Scalars['Boolean']>;
  /** Приоритет */
  priority?: InputMaybe<Scalars['Boolean']>;
  /** Подпись страницы */
  signature?: InputMaybe<Scalars['String']>;
  /** Теги на странице */
  tagNames?: InputMaybe<Array<Scalars['String']>>;
  /** Первоначальное добавление текста страницы */
  text?: InputMaybe<Scalars['String']>;
  /** Заголовок */
  title: Scalars['String'];
};

/** Добавление страницы */
export type AddPageMutationPayload = {
  __typename?: 'AddPageMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddPeriodGroupMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Название группы периода */
  name: Scalars['String'];
  /** Идентификатор периода */
  periodId: Scalars['ID'];
};

/** Мутация на добавление группы в период. */
export type AddPeriodGroupMutationPayload = {
  __typename?: 'AddPeriodGroupMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленная группа периода */
  periodGroup?: Maybe<PeriodGroupType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddPeriodMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** xlsx файл с проектом */
  file: Scalars['Upload'];
  /** Множественный тип сбора */
  multiple: Scalars['Boolean'];
  /** Название периода */
  name: Scalars['String'];
  /** Идентификатор проекта */
  projectId: Scalars['ID'];
  /** Запретить редактирование ячеек с заливкой */
  readonlyFillColor: Scalars['Boolean'];
  /** Разрешить множество версий */
  versioning: Scalars['Boolean'];
};

/** Мутация для создания периода. */
export type AddPeriodMutationPayload = {
  __typename?: 'AddPeriodMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленный период */
  period?: Maybe<PeriodType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddProfileMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Уникальный код настройки */
  code: Scalars['String'];
  /** Тип настройки: [0-3] */
  kind?: InputMaybe<Scalars['Int']>;
  /** Название настройки */
  name: Scalars['String'];
  /** Родительская настройка */
  parentId?: InputMaybe<Scalars['Int']>;
};

/** Мутация для добавления записи профиля. */
export type AddProfileMutationPayload = {
  __typename?: 'AddProfileMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленный профайл */
  profile?: Maybe<ProfileType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddProjectMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Тип дивизиона */
  contentType: Scalars['String'];
  /** Описание проекта */
  description: Scalars['String'];
  /** Наименование проекта */
  name: Scalars['String'];
  /** Сокращенное наименование проекта */
  short: Scalars['String'];
  /** Видимость проекта */
  visibility?: InputMaybe<Scalars['Boolean']>;
};

/** Мутация для добавления проекта. */
export type AddProjectMutationPayload = {
  __typename?: 'AddProjectMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленный проект */
  project?: Maybe<ProjectType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddRowDimensionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Индекс вставки в плоскую структуру */
  globalIndex: Scalars['Int'];
  /** Вспомогательные индексы в плоской структуре */
  globalIndices: Array<GlobalIndicesInputType>;
  /** Индекс вставки */
  index: Scalars['Int'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
};

/** Добавление строки. */
export type AddRowDimensionMutationPayload = {
  __typename?: 'AddRowDimensionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленная строка */
  rowDimension: RowDimensionType;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddSectionFilesMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемые изображения */
  files: Array<Scalars['Upload']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Текст страницы */
  text: Scalars['String'];
};

/** Добавление секции */
export type AddSectionFilesMutationPayload = {
  __typename?: 'AddSectionFilesMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Поле с файлами */
  section?: Maybe<SectionFilesType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddSectionGalleryMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемые изображения */
  images: Array<Scalars['Upload']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Текст страницы */
  text: Scalars['String'];
};

/** Добавление секции */
export type AddSectionGalleryMutationPayload = {
  __typename?: 'AddSectionGalleryMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Поле с файлами */
  section?: Maybe<SectionGalleryType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddSectionTextMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Текст страницы */
  text: Scalars['String'];
};

/** Добавление секции */
export type AddSectionTextMutationPayload = {
  __typename?: 'AddSectionTextMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Текстовое поле */
  section?: Maybe<SectionTextType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type AddTagMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  name: Scalars['String'];
};

/** Добавление тега */
export type AddTagMutationPayload = {
  __typename?: 'AddTagMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Добавленный тег */
  tag?: Maybe<TagType>;
};

/** An enumeration. */
export type ApplicationAlgorithm =
  /** No OIDC support */
  | 'A_'
  /** HMAC with SHA-2 256 */
  | 'HS256'
  /** RSA with SHA-2 256 */
  | 'RS256';

/** An enumeration. */
export type ApplicationAuthorizationGrantType =
  /** Authorization code */
  | 'AUTHORIZATION_CODE'
  /** Client credentials */
  | 'CLIENT_CREDENTIALS'
  /** Implicit */
  | 'IMPLICIT'
  /** OpenID connect hybrid */
  | 'OPENID_HYBRID'
  /** Resource owner password-based */
  | 'PASSWORD';

/** An enumeration. */
export type ApplicationClientType =
  /** Confidential */
  | 'CONFIDENTIAL'
  /** Public */
  | 'PUBLIC';

/** Приложение. */
export type ApplicationType = Node & {
  __typename?: 'ApplicationType';
  accesstokenSet: Array<AccessTokenType>;
  algorithm?: Maybe<ApplicationAlgorithm>;
  authorizationGrantType: ApplicationAuthorizationGrantType;
  clientId: Scalars['String'];
  clientSecret: Scalars['String'];
  clientType: ApplicationClientType;
  created: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  name: Scalars['String'];
  /** Allowed URIs list, space separated */
  redirectUris: Scalars['String'];
  skipAuthorization: Scalars['Boolean'];
  updated: Scalars['DateTime'];
  user?: Maybe<UserType>;
};

/** An enumeration. */
export type AttributeKind =
  /** bigMoney */
  | 'BIGMONEY'
  /** boolean */
  | 'BOOL'
  /** date */
  | 'DATE'
  /** files */
  | 'FILES'
  /** money */
  | 'MONEY'
  /** numeric */
  | 'NUMERIC'
  /** text */
  | 'TEXT';

/** Тип атрибутов для документов. */
export type AttributeType = {
  __typename?: 'AttributeType';
  /** Дочерние элементы */
  children?: Maybe<Array<Maybe<AttributeType>>>;
  /** Значение по умолчанию */
  default?: Maybe<Scalars['String']>;
  id: Scalars['ID'];
  /** Ключ */
  key: Scalars['String'];
  /** Тип атрибута */
  kind: AttributeKind;
  /** Можно ли изменять */
  mutable: Scalars['Boolean'];
  /** Наименование атрибута */
  name: Scalars['String'];
  /** Родительский атрибут */
  parent?: Maybe<AttributeType>;
  /** Период */
  period?: Maybe<PeriodType>;
  /** Подсказка */
  placeholder: Scalars['String'];
};

/** Тип со значениями атрибутов. */
export type AttributeValueType = {
  __typename?: 'AttributeValueType';
  /** Атрибут */
  attribute?: Maybe<AttributeType>;
  /** Идентификатор документа */
  attributeId?: Maybe<Scalars['Int']>;
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** Документ */
  document?: Maybe<DocumentType>;
  /** Идентификатор документа */
  documentId?: Maybe<Scalars['Int']>;
  id: Scalars['ID'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Значение */
  value: Scalars['String'];
};

export type AuthCbiasMutationInput = {
  /** Открытый идентификатор приложения */
  clientId?: InputMaybe<Scalars['String']>;
  /** Секретный идентификатор приложения */
  clientSecret?: InputMaybe<Scalars['String']>;
  /** Тип авторизации */
  grantType?: InputMaybe<Scalars['String']>;
  /** Идентификатор пользователя */
  uid: Scalars['String'];
};

export type AuthCbiasMutationOutput = {
  __typename?: 'AuthCbiasMutationOutput';
  /** Ошибки */
  errors?: Maybe<Array<Maybe<ErrorType>>>;
  /** Статус операции */
  success: Scalars['Boolean'];
  /** Информация о токене доступа */
  token?: Maybe<AuthTokenInfoType>;
  /** Авторизованный пользователь */
  user?: Maybe<UserType>;
};

/** Информация о сгенерированном токене доступа. */
export type AuthTokenInfoType = {
  __typename?: 'AuthTokenInfoType';
  /** Токен доступа */
  accessToken?: Maybe<Scalars['String']>;
  /** Время жизни токена */
  expiresIn?: Maybe<Scalars['Int']>;
  /** Переадресация при авторизации */
  redirectUris?: Maybe<Scalars['String']>;
  /** Токен обновления */
  refreshToken?: Maybe<Scalars['String']>;
  /** Разрешения */
  scope?: Maybe<Scalars['String']>;
  /** Тип токена */
  tokenType?: Maybe<Scalars['String']>;
};

/** Тип листа без структуры. */
export type BaseSheetType = {
  __typename?: 'BaseSheetType';
  /** Комментарий */
  comment: Scalars['String'];
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** Идентификатор */
  id: Scalars['ID'];
  /** Наименование */
  name: Scalars['String'];
  /** Период */
  period?: Maybe<PeriodType>;
  /** Позиция */
  position: Scalars['Int'];
  /** Показывать ли подведомственным */
  showChild: Scalars['Boolean'];
  /** Показвать ли головам */
  showHead: Scalars['Boolean'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
};

export type BudgetClassificationCodeFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type BudgetClassificationFilterInputType = {
  /** `And` field */
  and?: InputMaybe<Array<InputMaybe<BudgetClassificationFilterInputType>>>;
  /** `Code` field */
  code?: InputMaybe<BudgetClassificationCodeFilterInputType>;
  /** `Id` field */
  id?: InputMaybe<BudgetClassificationIdFilterInputType>;
  /** `Not` field */
  not?: InputMaybe<BudgetClassificationFilterInputType>;
  /** `Or` field */
  or?: InputMaybe<Array<InputMaybe<BudgetClassificationFilterInputType>>>;
};

export type BudgetClassificationIdFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['ID']>;
  /** `In` lookup */
  in?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

/** Graphene object type for budget classification codes. */
export type BudgetClassificationType = Node & {
  __typename?: 'BudgetClassificationType';
  /** Active */
  active: Scalars['Boolean'];
  /** Code */
  code: Scalars['String'];
  /** Created date */
  createdAt: Scalars['DateTime'];
  /** Date of end activity */
  end?: Maybe<Scalars['DateTime']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Name */
  name: Scalars['String'];
  /** Date of start activity */
  start: Scalars['DateTime'];
  /** Updated date */
  updatedAt: Scalars['DateTime'];
};

export type BudgetClassificationTypeConnection = {
  __typename?: 'BudgetClassificationTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<BudgetClassificationTypeEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `BudgetClassificationType` and its cursor. */
export type BudgetClassificationTypeEdge = {
  __typename?: 'BudgetClassificationTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<BudgetClassificationType>;
};

/** Категория */
export type CategoryType = Node & {
  __typename?: 'CategoryType';
  /** Аватар */
  avatar?: Maybe<Scalars['String']>;
  /** Дочерние категории */
  children: Array<Maybe<CategoryType>>;
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Соседние категории */
  nc: Array<Maybe<CategoryType>>;
  /** Страницы */
  pages?: Maybe<PageTypeConnection>;
  /** Родительская категория */
  parent?: Maybe<CategoryType>;
  /** Позиция вывода */
  position: Scalars['Int'];
  /** Текст */
  text: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

/** Категория */
export type CategoryTypePagesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  category_Id?: InputMaybe<Scalars['ID']>;
  first?: InputMaybe<Scalars['Int']>;
  kind_Id?: InputMaybe<Scalars['ID']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  title_Icontains?: InputMaybe<Scalars['String']>;
};

export type CategoryTypeConnection = {
  __typename?: 'CategoryTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<CategoryTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `CategoryType` and its cursor. */
export type CategoryTypeEdge = {
  __typename?: 'CategoryTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<CategoryType>;
};

/** Тип ячейки. */
export type CellType = {
  __typename?: 'CellType';
  /** Цвет фона */
  background: Scalars['String'];
  /** Цвет границ */
  borderColor: Scalars['JSONString'];
  /** Стили границ */
  borderStyle: Scalars['JSONString'];
  /** Цвет индекса */
  color: Scalars['String'];
  /** Объединение колонок */
  colspan: Scalars['Int'];
  /** Идентификатор колонки */
  columnId?: Maybe<Scalars['ID']>;
  /** Комментарий */
  comment?: Maybe<Scalars['String']>;
  /** Редактируемая ячейка */
  editable: Scalars['Boolean'];
  /** Текст ошибки */
  error?: Maybe<Scalars['String']>;
  /** Формула */
  formula?: Maybe<Scalars['String']>;
  /** Позиция в плоской структуре */
  globalPosition: Scalars['String'];
  /** Горизонтальное выравнивание */
  horizontalAlign?: Maybe<Scalars['ID']>;
  /** Идентификатор */
  id: Scalars['ID'];
  /** Курсив */
  italic: Scalars['Boolean'];
  /** Тип значения */
  kind: Scalars['String'];
  /** Маска для ввода значений */
  mask?: Maybe<Scalars['String']>;
  /** Позиция относительно родительской строки */
  position: Scalars['String'];
  /** Связанные с объединением позиции в плоской структуре */
  relatedGlobalPositions: Array<Scalars['String']>;
  /** Идентификатор строки */
  rowId?: Maybe<Scalars['ID']>;
  /** Объединение строк */
  rowspan: Scalars['Int'];
  /** Размер шрифта */
  size: Scalars['Int'];
  /** Зачеркнутый */
  strike: Scalars['Boolean'];
  /** Жирный шрифт */
  strong: Scalars['Boolean'];
  /** Подсказка */
  tooltip?: Maybe<Scalars['String']>;
  /** Тип подчеркивания */
  underline?: Maybe<Scalars['String']>;
  /** Значение */
  value?: Maybe<Scalars['String']>;
  /** Валидно ли поле */
  verified: Scalars['Boolean'];
  /** Вертикальное выравнивание */
  verticalAlign?: Maybe<Scalars['ID']>;
};

export type ChangeAttributeMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  default?: InputMaybe<Scalars['String']>;
  id?: InputMaybe<Scalars['ID']>;
  /** Ключ */
  key: Scalars['String'];
  /** Тип атрибута */
  kind: Scalars['String'];
  /** Можно ли изменять */
  mutable?: InputMaybe<Scalars['Boolean']>;
  /** Наименование атрибута */
  name: Scalars['String'];
  parent?: InputMaybe<Scalars['ID']>;
  /** Подсказка */
  placeholder: Scalars['String'];
  position?: InputMaybe<Scalars['Int']>;
};

/** Мутация для изменения периода. */
export type ChangeAttributeMutationPayload = {
  __typename?: 'ChangeAttributeMutationPayload';
  attribute?: Maybe<AttributeType>;
  clientMutationId?: Maybe<Scalars['String']>;
  errors?: Maybe<Array<Maybe<ErrorType>>>;
};

export type ChangeAttributeValueMutationInput = {
  /** Идентификатор атрибута */
  attributeId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор документа */
  documentId: Scalars['ID'];
  /** Значение атрибута. */
  value?: InputMaybe<Scalars['String']>;
};

/** Мутация для установки или изменения формы. */
export type ChangeAttributeValueMutationPayload = {
  __typename?: 'ChangeAttributeValueMutationPayload';
  /** Измененное или созданное значение */
  attributeValue?: Maybe<AttributeValueType>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Измененные значения листов */
  values?: Maybe<Array<Maybe<ValueType>>>;
};

export type ChangeAvatarMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемый файл аватара */
  file: Scalars['Upload'];
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
};

/** Мутация для изменения аватара пользователя. */
export type ChangeAvatarMutationPayload = {
  __typename?: 'ChangeAvatarMutationPayload';
  /** Загруженный аватар */
  avatar: Scalars['String'];
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeCategoryAvatarMutationInput = {
  /** Аватар */
  avatar?: InputMaybe<Scalars['Upload']>;
  /** Идентификатор мутации */
  categoryId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
};

/** Мутация для изменения аватара категории */
export type ChangeCategoryAvatarMutationPayload = {
  __typename?: 'ChangeCategoryAvatarMutationPayload';
  /** Добавленная котегория */
  category?: Maybe<CategoryType>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeCategoryMutationInput = {
  /** Идентификатор мутации */
  categoryId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Название категории */
  text: Scalars['String'];
};

/** Мутации для изменения категории */
export type ChangeCategoryMutationPayload = {
  __typename?: 'ChangeCategoryMutationPayload';
  /** Добавленная котегория */
  category?: Maybe<CategoryType>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeCategoryParentMutationInput = {
  /** Идентификатор категории */
  categoryId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор родителя */
  parentId?: InputMaybe<Scalars['ID']>;
};

/** Мутация для изменения родителя */
export type ChangeCategoryParentMutationPayload = {
  __typename?: 'ChangeCategoryParentMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeCategoryPositionMutationInput = {
  /** Идентификаторы категорий */
  categoriesId: Array<InputMaybe<Scalars['ID']>>;
  clientMutationId?: InputMaybe<Scalars['String']>;
};

/** Мутация для изменения порядка следования вывода категорий */
export type ChangeCategoryPositionMutationPayload = {
  __typename?: 'ChangeCategoryPositionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeCellDefaultInput = {
  /** Идентификатор ячейки */
  cellId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Значение по умолчанию */
  default: Scalars['String'];
};

/** Изменение значения ячейки по умолчанию. */
export type ChangeCellDefaultPayload = {
  __typename?: 'ChangeCellDefaultPayload';
  /** Идентификатор ячейки */
  cellId: Scalars['ID'];
  clientMutationId?: Maybe<Scalars['String']>;
  /** Значение по умолчанию */
  default: Scalars['String'];
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeCellsOptionMutationInput = {
  /** Идентификаторы ячеек */
  cellIds: Array<Scalars['ID']>;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор поля */
  field: Scalars['String'];
  /** Значение поля */
  value?: InputMaybe<Scalars['String']>;
};

/**
 * Изменение свойств ячеек:
 *
 * - strong - true, false
 * - italic - true, false
 * - strike - true, false
 * - underline - [None, 'single', 'double', 'single_accounting', 'double_accounting']
 * - horizontal_align - ['left', 'center', 'right']
 * - vertical_align - ['top', 'middle', 'bottom']
 * - size - число от 6 до 24
 * - kind - [
 *     'n', 's', 'f', 'b', 'inlineStr', 'e', 'str', 'd', 'text', 'money',
 *     'bigMoney', 'fl', 'user', 'department', 'organization', 'classification'
 * ]
 */
export type ChangeCellsOptionMutationPayload = {
  __typename?: 'ChangeCellsOptionMutationPayload';
  /** Измененные свойства ячеек */
  changedOptions?: Maybe<Array<ChangedCellOption>>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeChildRowDimensionHeightMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Высота строки */
  height?: InputMaybe<Scalars['Int']>;
  /** Идентификатор строки */
  rowDimensionId: Scalars['ID'];
};

/** Изменение высоты дочерней строки. */
export type ChangeChildRowDimensionHeightMutationPayload = {
  __typename?: 'ChangeChildRowDimensionHeightMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Высота строки */
  height?: Maybe<Scalars['Int']>;
  /** Идентификатор строки */
  rowDimensionId: Scalars['ID'];
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Дата обновления строки */
  updatedAt: Scalars['DateTime'];
};

export type ChangeColumnDimensionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор колонки */
  columnDimensionId: Scalars['ID'];
  /** Скрытие колонки */
  hidden: Scalars['Boolean'];
  /** Тип значения */
  kind: Scalars['String'];
  /** Ширина колонки */
  width?: InputMaybe<Scalars['Int']>;
};

/** Изменение колонки. */
export type ChangeColumnDimensionMutationPayload = {
  __typename?: 'ChangeColumnDimensionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Измененная колонка */
  columnDimension?: Maybe<ChangeColumnDimensionType>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeColumnDimensionType = {
  __typename?: 'ChangeColumnDimensionType';
  /** Фиксация колонки */
  fixed: Scalars['Boolean'];
  /** Скрытие колонки */
  hidden: Scalars['Boolean'];
  id: Scalars['ID'];
  /** Тип значений */
  kind: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Ширина колонки */
  width?: Maybe<Scalars['Int']>;
};

export type ChangeColumnDimensionsFixedInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификаторы колонок */
  columnDimensionIds: Array<Scalars['ID']>;
  /** Фиксация колонки */
  fixed: Scalars['Boolean'];
};

/** Изменение свойства fixed у колонок. */
export type ChangeColumnDimensionsFixedPayload = {
  __typename?: 'ChangeColumnDimensionsFixedPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Измененные колонки */
  columnDimensions?: Maybe<Array<Maybe<ChangeColumnDimensionType>>>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeDocumentCommentMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Комментарий */
  comment: Scalars['String'];
  /** Идентификатор документа */
  documentId?: InputMaybe<Scalars['ID']>;
};

/** Изменение комментария версии документа. */
export type ChangeDocumentCommentMutationPayload = {
  __typename?: 'ChangeDocumentCommentMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Созданный документ */
  document?: Maybe<DocumentType>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeFileMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Поле файла */
  field: Scalars['String'];
  /** Идентификатор файла */
  fileId: Scalars['ID'];
  /** Значение поля файла */
  value: Scalars['String'];
};

/** Мутация для изменения файла */
export type ChangeFileMutationPayload = {
  __typename?: 'ChangeFileMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененный файл */
  file?: Maybe<FileType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeFileValueMutationInput = {
  /** Идентификатор ячейки */
  cellId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор документа */
  documentId: Scalars['ID'];
  /** Новые файлы */
  newFiles: Array<Scalars['Upload']>;
  /** Оставшиеся файлы */
  remainingFiles: Array<Scalars['ID']>;
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
  /** Значение */
  value: Scalars['String'];
};

/** Изменение значения ячейки типа `Файл`. */
export type ChangeFileValueMutationPayload = {
  __typename?: 'ChangeFileValueMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Дата изменения */
  updatedAt: Scalars['DateTime'];
  /** Измененное значение */
  value: Scalars['String'];
  /** Измененные файлы */
  valueFiles?: Maybe<Array<Maybe<FileType>>>;
};

export type ChangeGroupNameMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор группы */
  groupId: Scalars['Int'];
  /** Название группы */
  name: Scalars['String'];
};

/** Мутация для изменения имени группы. */
export type ChangeGroupNameMutationPayload = {
  __typename?: 'ChangeGroupNameMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная группа */
  group?: Maybe<GroupType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeGroupPermissionsMutationInput = {
  /** Действие */
  action: ActionRelationShip;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор группы */
  groupId: Scalars['Int'];
  /** Идентификаторы привилегий */
  permissionsId: Array<InputMaybe<Scalars['Int']>>;
};

/** Мутация для изменения привилегий группы. */
export type ChangeGroupPermissionsMutationPayload = {
  __typename?: 'ChangeGroupPermissionsMutationPayload';
  /** Действие */
  action: ActionRelationShip;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Идентификаторы привилегий */
  permissionsId: Array<Maybe<Scalars['Int']>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeNotificationMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Название поля */
  field: Scalars['String'];
  /** Идентификатор уведомления */
  notificationId: Scalars['ID'];
  /** Значение */
  value: Scalars['Boolean'];
};

/** Изменение уведомления */
export type ChangeNotificationMutationPayload = {
  __typename?: 'ChangeNotificationMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeNotificationsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Название поля */
  field: Scalars['String'];
  /** Идентификаторы уведомлений */
  notificationsId: Array<InputMaybe<Scalars['ID']>>;
  /** Значение */
  value: Scalars['Boolean'];
};

/** Изменение всех уведомлений */
export type ChangeNotificationsMutationPayload = {
  __typename?: 'ChangeNotificationsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePageAvatarMutationInput = {
  /** Новый аватар страницы */
  avatar?: InputMaybe<Scalars['Upload']>;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
};

/** Изменение аватара на странице */
export type ChangePageAvatarMutationPayload = {
  __typename?: 'ChangePageAvatarMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePageBooleanPropertyMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  field: Scalars['String'];
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Значение */
  value: Scalars['Boolean'];
};

/** Изменение boolean свойств страницы */
export type ChangePageBooleanPropertyMutationPayload = {
  __typename?: 'ChangePageBooleanPropertyMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePageCategoryMutationInput = {
  /** Идентификатор категории */
  categoryId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
};

/** Изменение категории страницы */
export type ChangePageCategoryMutationPayload = {
  __typename?: 'ChangePageCategoryMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePageKindMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Идентификатор типа страницы */
  pageKindId?: InputMaybe<Scalars['Int']>;
};

/** Изменение типа страницы */
export type ChangePageKindMutationPayload = {
  __typename?: 'ChangePageKindMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePageTagsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Теги */
  tagNames: Array<Scalars['String']>;
};

/** Изменения тегов страницы */
export type ChangePageTagsMutationPayload = {
  __typename?: 'ChangePageTagsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePageTitleMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор страницы */
  pageId: Scalars['ID'];
  /** Заголовок страницы */
  title: Scalars['String'];
};

/** Изменение названия страницы */
export type ChangePageTitleMutationPayload = {
  __typename?: 'ChangePageTitleMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная страница */
  page?: Maybe<PageType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePasswordMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Старый пароль */
  password: Scalars['String'];
  /** Новый пароль */
  passwordNew: Scalars['String'];
};

/** Мутация для изменения пароля пользователя. */
export type ChangePasswordMutationPayload = {
  __typename?: 'ChangePasswordMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePeriodGroupPrivilegesMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор группы периода */
  periodGroupId: Scalars['ID'];
  /** Идентификаторы привилегий */
  privilegesIds?: InputMaybe<Array<Scalars['ID']>>;
};

/** Мутация на изменение привилегий группы. */
export type ChangePeriodGroupPrivilegesMutationPayload = {
  __typename?: 'ChangePeriodGroupPrivilegesMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Привилегии группы */
  privileges: Array<Maybe<PrivilegeType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangePeriodMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Дата окончания */
  expiration?: InputMaybe<Scalars['Date']>;
  /** Множественное заполнение */
  multiple: Scalars['Boolean'];
  /** Название периода */
  name: Scalars['String'];
  /** Идентификатор текущего периода */
  periodId: Scalars['ID'];
  /** Приватность полей */
  privately: Scalars['Boolean'];
  /** Дата начала */
  start?: InputMaybe<Scalars['Date']>;
  /** Статус проекта */
  status: Scalars['String'];
  /** Разрешить множество версий */
  versioning: Scalars['Boolean'];
};

/** Мутация на изменение настроек периода. */
export type ChangePeriodMutationPayload = {
  __typename?: 'ChangePeriodMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененный период */
  period?: Maybe<PeriodType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeProfileValueMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор записи профиля */
  profileId: Scalars['ID'];
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
  /** Значение записи */
  value: Scalars['String'];
};

/** Мутация на изменение значения профиля. */
export type ChangeProfileValueMutationPayload = {
  __typename?: 'ChangeProfileValueMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Добавленное значение профиля */
  profileValue?: Maybe<ProfileValueType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeProfileVisibilityMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор записи */
  profileValueId: Scalars['ID'];
  /** Значение доступности */
  visibility: Scalars['Boolean'];
};

/** Матция для изменения видимости. */
export type ChangeProfileVisibilityMutationPayload = {
  __typename?: 'ChangeProfileVisibilityMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененное значение поля */
  profileValue?: Maybe<ProfileValueType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeProjectMutationInput = {
  /** Архив */
  archive?: InputMaybe<Scalars['Boolean']>;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Описание проекта */
  description?: InputMaybe<Scalars['String']>;
  /** Наименование проекта */
  name?: InputMaybe<Scalars['String']>;
  /** Идентификатор проекта */
  projectId: Scalars['ID'];
  /** Сокращенное наименование проекта */
  short?: InputMaybe<Scalars['String']>;
  /** Видимость проекта */
  visibility?: InputMaybe<Scalars['Boolean']>;
};

/** Мутация изменения настроек проекта. */
export type ChangeProjectMutationPayload = {
  __typename?: 'ChangeProjectMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененный проект */
  project?: Maybe<ProjectType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeRowDimensionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Динамическая ли строка */
  dynamic: Scalars['Boolean'];
  /** Высота строки */
  height?: InputMaybe<Scalars['Int']>;
  /** Скрытие строки */
  hidden: Scalars['Boolean'];
  /** Идентификатор строки */
  rowDimensionId: Scalars['ID'];
};

/** Изменение строки. */
export type ChangeRowDimensionMutationPayload = {
  __typename?: 'ChangeRowDimensionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная строка */
  rowDimension?: Maybe<ChangeRowDimensionType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeRowDimensionType = {
  __typename?: 'ChangeRowDimensionType';
  /** Динамическая ли строка */
  dynamic: Scalars['Boolean'];
  /** Фиксация строки */
  fixed: Scalars['Boolean'];
  /** Высота строки */
  height?: Maybe<Scalars['Int']>;
  /** Скрытие строки */
  hidden: Scalars['Boolean'];
  id: Scalars['ID'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
};

export type ChangeRowDimensionsFixedInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Фиксация строки */
  fixed: Scalars['Boolean'];
  /** Идентификаторы строк */
  rowDimensionIds: Array<Scalars['ID']>;
};

/** Изменение свойства fixed у строк. */
export type ChangeRowDimensionsFixedPayload = {
  __typename?: 'ChangeRowDimensionsFixedPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененные строки */
  rowDimensions?: Maybe<Array<Maybe<ChangeRowDimensionType>>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeSectionFilesMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемые изображения */
  newFiles?: InputMaybe<Array<Scalars['Upload']>>;
  /** Изображения */
  oldFiles: Array<Scalars['ID']>;
  /** Идентификатор секции */
  sectionId: Scalars['ID'];
  /** Текст мутации */
  text: Scalars['String'];
};

/** Изменение текста секции */
export type ChangeSectionFilesMutationPayload = {
  __typename?: 'ChangeSectionFilesMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Секция галереи */
  section?: Maybe<SectionFilesType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeSectionGalleryMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемые изображения */
  newImages?: InputMaybe<Array<Scalars['Upload']>>;
  /** Изображения */
  oldImages: Array<Scalars['ID']>;
  /** Идентификатор секции */
  sectionId: Scalars['ID'];
  /** Текст мутации */
  text: Scalars['String'];
};

/** Изменение текста секции */
export type ChangeSectionGalleryMutationPayload = {
  __typename?: 'ChangeSectionGalleryMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Секция галереи */
  section?: Maybe<SectionGalleryType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeSectionTextMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор секции */
  sectionId: Scalars['ID'];
  /** Текст мутации */
  text: Scalars['String'];
};

/** Изменение текста секции */
export type ChangeSectionTextMutationPayload = {
  __typename?: 'ChangeSectionTextMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Текстовая секция */
  section?: Maybe<SectionTextType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeSettingsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор настройки */
  key: Scalars['String'];
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
  /** Значение настройки */
  value: Scalars['String'];
};

/** Мутация для изменения настроек */
export type ChangeSettingsMutationPayload = {
  __typename?: 'ChangeSettingsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененная настройка */
  setting?: Maybe<SettingType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeShowSheetMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Выбор: showHead, showChild */
  field: Scalars['String'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
  /** Значение */
  value: Scalars['Boolean'];
};

/** Изменение показа листа. */
export type ChangeShowSheetMutationPayload = {
  __typename?: 'ChangeShowSheetMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Измененный лист */
  sheet?: Maybe<BaseSheetType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeUserGroupsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор групп */
  groupsId: Array<InputMaybe<Scalars['Int']>>;
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
};

/** Мутация для изменения групп конкретного пользователя. */
export type ChangeUserGroupsMutationPayload = {
  __typename?: 'ChangeUserGroupsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Новые группы */
  groups?: Maybe<Array<Maybe<GroupType>>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type ChangeUserPeriodGroupsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификаторы групп пользователя в периоде */
  periodGroupIds?: InputMaybe<Array<Scalars['ID']>>;
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
};

/** Мутация на изменение групп пользователя в периоде. */
export type ChangeUserPeriodGroupsMutationPayload = {
  __typename?: 'ChangeUserPeriodGroupsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Группы пользователя */
  periodGroups: Array<Maybe<PeriodGroupType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Пользователь */
  user: UserType;
};

export type ChangeUserPeriodPrivilegesMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор периода */
  periodId: Scalars['ID'];
  /** Идентификаторы привилегий пользователя в периоде */
  privilegesIds?: InputMaybe<Array<Scalars['ID']>>;
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
};

/** Мутация на изменение отдельных привилегий пользователя в периоде. */
export type ChangeUserPeriodPrivilegesMutationPayload = {
  __typename?: 'ChangeUserPeriodPrivilegesMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Привилегии пользователя в периоде */
  privileges: Array<Maybe<PrivilegeType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Пользователь */
  user: UserType;
};

export type ChangeUserPropsMutationInput = {
  /** Дата рождения */
  birthday: Scalars['Date'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Email */
  email: Scalars['String'];
  /** Имя */
  firstName: Scalars['String'];
  /** Фамилия */
  lastName: Scalars['String'];
  /** Отчество */
  sirName: Scalars['String'];
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
};

/** Мутация для изменения полей пользователя. */
export type ChangeUserPropsMutationPayload = {
  __typename?: 'ChangeUserPropsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Измененный пользователь */
  user: UserType;
};

export type ChangeValueMutationInput = {
  /** Идентификатор ячейки */
  cellId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор документа */
  documentId: Scalars['ID'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
  /** Значение */
  value: Scalars['String'];
};

/** Изменение значения ячейки. */
export type ChangeValueMutationPayload = {
  __typename?: 'ChangeValueMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Дата изменения */
  updatedAt?: Maybe<Scalars['DateTime']>;
  /** Измененные ячейки */
  values?: Maybe<Array<Maybe<ValueType>>>;
};

/** Измененное свойство ячейки. */
export type ChangedCellOption = {
  __typename?: 'ChangedCellOption';
  /** Идентификаторы ячеек */
  cellId: Scalars['ID'];
  /** Идентификатор поля */
  field: Scalars['String'];
  /** Значение поля */
  value?: Maybe<Scalars['String']>;
};

/** Тип колонки. */
export type ColumnDimensionType = {
  __typename?: 'ColumnDimensionType';
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** Фиксация колонки */
  fixed: Scalars['Boolean'];
  /** Скрытие колонки */
  hidden: Scalars['Boolean'];
  /** Идентификатор */
  id: Scalars['ID'];
  /** Индекс колонки */
  index: Scalars['Int'];
  /** Тип значений */
  kind: Scalars['String'];
  /** Название колонки */
  name: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Идентификатор пользователя */
  userId?: Maybe<Scalars['ID']>;
  /** Ширина колонки */
  width?: Maybe<Scalars['Int']>;
};

/** Комментарии */
export type CommentType = Node & {
  __typename?: 'CommentType';
  /** Дочерние комментарии */
  children: Array<Maybe<CategoryType>>;
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Страница */
  page: PageType;
  /** Рейтинг */
  rating: Scalars['Int'];
  /** Текст */
  text: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь, оставивший комментарий */
  user: UserType;
};

export type CommentTypeConnection = {
  __typename?: 'CommentTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<CommentTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `CommentType` and its cursor. */
export type CommentTypeEdge = {
  __typename?: 'CommentTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<CommentType>;
};

export type ConfirmEmailMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Код, полученный по Email */
  code: Scalars['String'];
  /** Email адрес */
  email: Scalars['String'];
};

/** Подтверждение кода. */
export type ConfirmEmailMutationPayload = {
  __typename?: 'ConfirmEmailMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

/**
 * Типы уведомления пользователей
 * - CONNECT - Присоединился
 * - DISCONNECT - Отсоединился
 * - ADD - Пользователь добавил данные (по умолчанию)
 * - CHANGE - Пользователь изменил данные
 * - DELETE - Удаление объекта
 * - ERROR - Ошибка ввода данных
 * - TYPING - Печатет, готовиться отправить сообщение
 * - TYPING_FINISH - Закончил печатать
 * - EXCEPTION - Пользователь исключен из потока уведомлений
 */
export type ConsumerActionType =
  | 'ADD'
  | 'CHANGE'
  | 'CONNECT'
  | 'DELETE'
  | 'DISCONNECT'
  | 'ERROR'
  | 'EXCEPTION'
  | 'TYPING'
  | 'TYPING_FINISH';

/** Тип модели Django. */
export type ContentTypeType = {
  __typename?: 'ContentTypeType';
  appLabel: Scalars['String'];
  id: Scalars['ID'];
  model: Scalars['String'];
  permissionSet: Array<PermissionType>;
  /** Тип дивизиона */
  projectSet: ProjectTypeConnection;
};

/** Тип модели Django. */
export type ContentTypeTypeProjectSetArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  name_Icontains?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
  user?: InputMaybe<Scalars['ID']>;
  user_In?: InputMaybe<Array<InputMaybe<Scalars['ID']>>>;
};

export type CopyPeriodGroupsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Выбранные группы */
  periodGroupIds: Array<Scalars['ID']>;
  /** Идентификатор текущего периода */
  periodId: Scalars['ID'];
  /** Идентификатор выбранного периода */
  selectedPeriodId: Scalars['ID'];
};

/** Мутация на перенос групп с пользователями из другого периода. */
export type CopyPeriodGroupsMutationPayload = {
  __typename?: 'CopyPeriodGroupsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Новые группы периода */
  periodGroups: Array<Maybe<PeriodGroupType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Информация по показателям во временной развертке. */
export type DateStatisticsType = {
  __typename?: 'DateStatisticsType';
  /** Дата */
  date: Scalars['Date'];
  /** Значение */
  value: Scalars['Float'];
};

export type DeleteAttributeMutationInput = {
  /**
   * Идентификатор модели "Не табличные данные хранятся в атрибутах.
   *
   *     Модель содержит список не табличных данных для организации сбора в указанный период.
   *     Информация о типах:
   *         - TEXT - тестовое поле
   *         - MONEY - поле для ввода денег
   *     "
   */
  attributeId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
};

/** Удаление записи модели "Attribute" */
export type DeleteAttributeMutationPayload = {
  __typename?: 'DeleteAttributeMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteCategoryMutationInput = {
  /** Идентификатор мутации */
  categoryId: Scalars['ID'];
  clientMutationId?: InputMaybe<Scalars['String']>;
};

/** Мутация для удаления категории */
export type DeleteCategoryMutationPayload = {
  __typename?: 'DeleteCategoryMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteChildRowDimensionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор строки */
  rowDimensionId: Scalars['ID'];
};

/** Удаление дочерней строки. */
export type DeleteChildRowDimensionMutationPayload = {
  __typename?: 'DeleteChildRowDimensionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Идентификатор удаленной строки */
  rowDimensionId: Scalars['ID'];
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteDivisionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор дивизиона */
  divisionId: Scalars['ID'];
  /** Идентификатор периода */
  periodId: Scalars['ID'];
};

/** Мутация на удаление дивизиона из периода. */
export type DeleteDivisionMutationPayload = {
  __typename?: 'DeleteDivisionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Идентификатор удаленного дивизиона */
  deleteId: Scalars['ID'];
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteDocumentStatusMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор статуса документа */
  documentStatusId: Scalars['ID'];
};

/** Удаление статуса документа. */
export type DeleteDocumentStatusMutationPayload = {
  __typename?: 'DeleteDocumentStatusMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Идентификатор статуса документа */
  id: Scalars['ID'];
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteFileMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор файла */
  fileId: Scalars['ID'];
};

/** Мутация для полного удаления файла */
export type DeleteFileMutationPayload = {
  __typename?: 'DeleteFileMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Идентификатор удаляемого файла */
  id: Scalars['ID'];
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteGroupMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор группы */
  groupId: Scalars['Int'];
};

/** Мутация для удаления группы. */
export type DeleteGroupMutationPayload = {
  __typename?: 'DeleteGroupMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Идентификатор группы */
  id: Scalars['ID'];
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteNoticeMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор уведомления */
  noticeId: Scalars['ID'];
};

/** Удаление всех уведомлений */
export type DeleteNoticeMutationPayload = {
  __typename?: 'DeleteNoticeMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeletePageMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  pageId: Scalars['ID'];
};

/** Удаление страницы */
export type DeletePageMutationPayload = {
  __typename?: 'DeletePageMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeletePeriodGroupMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор группы периода */
  periodGroupId: Scalars['ID'];
};

/** Мутация на удаление группы периода. */
export type DeletePeriodGroupMutationPayload = {
  __typename?: 'DeletePeriodGroupMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Идентификатор удаленной группы периода */
  deleteId: Scalars['ID'];
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeletePeriodMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор периода */
  periodId: Scalars['ID'];
};

/** Мутация на удаление периода. */
export type DeletePeriodMutationPayload = {
  __typename?: 'DeletePeriodMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Идентификатор удаленного периода */
  deleteId: Scalars['ID'];
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteProfileMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор записи */
  profileId: Scalars['Int'];
};

/** Мутация для удаления записи профиля. */
export type DeleteProfileMutationPayload = {
  __typename?: 'DeleteProfileMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteProjectMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор проекта */
  projectId: Scalars['ID'];
};

/** Мутация на удаление проекта. */
export type DeleteProjectMutationPayload = {
  __typename?: 'DeleteProjectMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Идентификатор удаленного проекта */
  deleteId: Scalars['ID'];
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteRowDimensionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор строки */
  rowDimensionId: Scalars['ID'];
};

/** Удаление строки. */
export type DeleteRowDimensionMutationPayload = {
  __typename?: 'DeleteRowDimensionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Идентификатор удаленной строки */
  rowDimensionId: Scalars['ID'];
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteSectionMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор секции */
  sectionId: Scalars['ID'];
};

/** Удаление секции */
export type DeleteSectionMutationPayload = {
  __typename?: 'DeleteSectionMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type DeleteSessionsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
};

/** Мутация для удаления всех сессий кроме текущей. */
export type DeleteSessionsMutationPayload = {
  __typename?: 'DeleteSessionsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Graphene object type for Department. */
export type DepartmentType = {
  __typename?: 'DepartmentType';
  /** Children departments. */
  children?: Maybe<Array<Maybe<DepartmentType>>>;
  /** Code of department */
  code?: Maybe<Scalars['Int']>;
  /** Created date */
  createdAt: Scalars['DateTime'];
  id: Scalars['ID'];
  /** Responsible Minister. */
  minister: UserType;
  /** Department name */
  name: Scalars['String'];
  /** Organizations. */
  organizations?: Maybe<Array<Maybe<OrganizationType>>>;
  /** Updated date */
  updatedAt: Scalars['DateTime'];
  /** Director of department. */
  user: UserType;
  /** Department staff. */
  users?: Maybe<Array<Maybe<UserType>>>;
};

/** Graphene object type for District. */
export type DistrictType = {
  __typename?: 'DistrictType';
  /** Created date */
  createdAt: Scalars['DateTime'];
  id: Scalars['ID'];
  /** District name */
  name: Scalars['String'];
  /** List of regions. */
  regions?: Maybe<Array<Maybe<RegionType>>>;
  /** Updated date */
  updatedAt: Scalars['DateTime'];
};

/** Описание обобщенного типа дивизиона. */
export type DivisionModelType = Node & {
  __typename?: 'DivisionModelType';
  /** Идентификатор модели дивизиона */
  id: Scalars['ID'];
  /** Модель дивизиона: department, organization */
  model: Scalars['String'];
  /** Название дивизиона */
  name: Scalars['String'];
};

/** Connection для обобщенного типа дивизиона. */
export type DivisionModelTypeConnection = {
  __typename?: 'DivisionModelTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<DivisionModelTypeEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
};

/** A Relay edge containing a `DivisionModelType` and its cursor. */
export type DivisionModelTypeEdge = {
  __typename?: 'DivisionModelTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<DivisionModelType>;
};

/** Debugging information for the current query. */
export type DjangoDebug = {
  __typename?: 'DjangoDebug';
  /** Executed SQL queries for this API query. */
  sql?: Maybe<Array<Maybe<DjangoDebugSql>>>;
};

/** Represents a single database query made to a Django managed DB. */
export type DjangoDebugSql = {
  __typename?: 'DjangoDebugSQL';
  /** The Django database alias (e.g. 'default'). */
  alias: Scalars['String'];
  /** Duration of this database query in seconds. */
  duration: Scalars['Float'];
  /** Postgres connection encoding if available. */
  encoding?: Maybe<Scalars['String']>;
  /** Whether this database query was a SELECT. */
  isSelect: Scalars['Boolean'];
  /** Whether this database query took more than 10 seconds. */
  isSlow: Scalars['Boolean'];
  /** Postgres isolation level if available. */
  isoLevel?: Maybe<Scalars['String']>;
  /** JSON encoded database query parameters. */
  params: Scalars['String'];
  /** The raw SQL of this query, without params. */
  rawSql: Scalars['String'];
  /** The actual SQL sent to this database. */
  sql?: Maybe<Scalars['String']>;
  /** Start time of this database query. */
  startTime: Scalars['Float'];
  /** Stop time of this database query. */
  stopTime: Scalars['Float'];
  /** Postgres transaction ID if available. */
  transId?: Maybe<Scalars['String']>;
  /** Postgres transaction status if available. */
  transStatus?: Maybe<Scalars['String']>;
  /** The type of database being used (e.g. postrgesql, mysql, sqlite). */
  vendor: Scalars['String'];
};

/** Тип статусов для документов. */
export type DocumentStatusType = {
  __typename?: 'DocumentStatusType';
  /** Комментарий */
  comment: Scalars['String'];
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** Документ */
  document?: Maybe<DocumentType>;
  id: Scalars['ID'];
  /** Установленный статус */
  status: StatusType;
  /** Пользователь */
  user: UserType;
};

/** Тип моделей документа. */
export type DocumentType = Node & {
  __typename?: 'DocumentType';
  /** Может ли пользователь изменять документ */
  canChange: Scalars['Boolean'];
  /** Может ли пользователь удалять документ */
  canDelete: Scalars['Boolean'];
  /** Комментарий */
  comment: Scalars['String'];
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Последний статус документа */
  lastStatus?: Maybe<DocumentStatusType>;
  /** Идентификатор дивизиона */
  objectId?: Maybe<Scalars['ID']>;
  /** Название дивизиона */
  objectName?: Maybe<Scalars['String']>;
  /** Период сбора */
  period?: Maybe<PeriodType>;
  /** Листы */
  sheets: Array<Maybe<BaseSheetType>>;
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь, добавивший документ */
  user?: Maybe<UserType>;
  /** Версия документа */
  version: Scalars['Int'];
};

export type DocumentTypeConnection = {
  __typename?: 'DocumentTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<DocumentTypeEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `DocumentType` and its cursor. */
export type DocumentTypeEdge = {
  __typename?: 'DocumentTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<DocumentType>;
};

/** Ошибка в поле формы */
export type ErrorFieldType = {
  __typename?: 'ErrorFieldType';
  /** Поле формы */
  field: Scalars['String'];
  /** Ошибки */
  messages: Array<Scalars['String']>;
};

export type ErrorType = {
  __typename?: 'ErrorType';
  field: Scalars['String'];
  messages: Array<Scalars['String']>;
};

/** Файл пользователя. */
export type FileType = Node & {
  __typename?: 'FileType';
  /** Дата добавления файла */
  createdAt: Scalars['DateTime'];
  /** Помечаем удаленный файл */
  deleted: Scalars['Boolean'];
  /** Расширение файла */
  ext?: Maybe<Scalars['String']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Название файла */
  name: Scalars['String'];
  /** Размер файла в байтах */
  size?: Maybe<Scalars['Int']>;
  /** Путь к файлу */
  src: Scalars['String'];
  /** Дата обновления файла */
  updatedAt: Scalars['DateTime'];
  /** Пользователь, добавивший файл */
  user?: Maybe<UserType>;
};

export type FileTypeConnection = {
  __typename?: 'FileTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<FileTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `FileType` and its cursor. */
export type FileTypeEdge = {
  __typename?: 'FileTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<FileType>;
};

export type GetTokenMutationInput = {
  /** Открытый идентификатор приложения */
  clientId?: InputMaybe<Scalars['String']>;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Секретный идентификатор приложения */
  clientSecret?: InputMaybe<Scalars['String']>;
  /** Тип авторизации */
  grantType?: InputMaybe<Scalars['String']>;
  /** Пароль */
  password?: InputMaybe<Scalars['String']>;
  /** Имя пользователя */
  username?: InputMaybe<Scalars['String']>;
};

/** Мутация для получения токена авторизации. */
export type GetTokenMutationPayload = {
  __typename?: 'GetTokenMutationPayload';
  /** Токен доступа */
  accessToken?: Maybe<Scalars['String']>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Время жизни токена */
  expiresIn?: Maybe<Scalars['Int']>;
  /** Токен обновления */
  refreshToken?: Maybe<Scalars['String']>;
  /** Разрешения */
  scope?: Maybe<Scalars['String']>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Тип токена */
  tokenType?: Maybe<Scalars['String']>;
  /** Авторизованный пользователь */
  user?: Maybe<UserType>;
};

/** Индекс строки в плоской структуре. */
export type GlobalIndicesInputType = {
  /** Индекс в плоской структуре */
  globalIndex: Scalars['Int'];
  /** Идентификатор строки */
  rowId: Scalars['ID'];
};

/** Группа пользователей. */
export type GroupType = {
  __typename?: 'GroupType';
  id: Scalars['ID'];
  name: Scalars['String'];
  permissions: Array<PermissionType>;
  /** Группы, к которым принадлежит данный пользователь. Пользователь получит все права, указанные в каждой из его/её групп. */
  userSet: UserTypeConnection;
};

/** Группа пользователей. */
export type GroupTypeUserSetArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  email_Icontains?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  firstName_Icontains?: InputMaybe<Scalars['String']>;
  last?: InputMaybe<Scalars['Int']>;
  lastName_Icontains?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
  sirName_Icontains?: InputMaybe<Scalars['String']>;
  username_Icontains?: InputMaybe<Scalars['String']>;
};

/** An enumeration. */
export type LogEntryAction =
  /** create */
  | 'A_0'
  /** update */
  | 'A_1'
  /** delete */
  | 'A_2';

/** Логирование действия пользователя. */
export type LogEntryType = Node & {
  __typename?: 'LogEntryType';
  action: LogEntryAction;
  /** Модель, связанная с действием */
  contentType?: Maybe<ContentTypeType>;
  /** Дата и время действия */
  createdAt?: Maybe<Scalars['DateTime']>;
  /** The ID of the object. */
  id: Scalars['ID'];
  objectId?: Maybe<Scalars['Int']>;
  /** Измененные данные */
  payload?: Maybe<Scalars['String']>;
  /** Сессия пользователя */
  session?: Maybe<SessionType>;
};

export type LogEntryTypeConnection = {
  __typename?: 'LogEntryTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<LogEntryTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `LogEntryType` and its cursor. */
export type LogEntryTypeEdge = {
  __typename?: 'LogEntryTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<LogEntryType>;
};

/** Лог запроса. */
export type LogRequestType = Node & {
  __typename?: 'LogRequestType';
  /** Дата и время запроса */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Страница, с которой отправлен запрос */
  page?: Maybe<Scalars['String']>;
  /** Сессия пользователя */
  session?: Maybe<SessionType>;
  /** Время работы страницы */
  time: Scalars['Float'];
};

export type LogRequestTypeConnection = {
  __typename?: 'LogRequestTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<LogRequestTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `LogRequestType` and its cursor. */
export type LogRequestTypeEdge = {
  __typename?: 'LogRequestTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<LogRequestType>;
};

export type LogoutMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор сессии */
  sessionId: Scalars['ID'];
};

/** Мутация выхода */
export type LogoutMutationPayload = {
  __typename?: 'LogoutMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Оповещение */
export type MailingType = {
  __typename?: 'MailingType';
  /** Адрес отправки */
  address: Scalars['String'];
  /** Массив прикрепленных файлов */
  attachments?: Maybe<Scalars['JSONString']>;
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** Средства отправки */
  dispatchers: Scalars['JSONString'];
  /** Заголовок сообщения */
  header: Scalars['String'];
  id: Scalars['ID'];
  /** Текст сообщения */
  text: Scalars['String'];
  /** Пользователь */
  user: UserType;
};

/** Мутации на изменение чего-либо. */
export type Mutation = {
  __typename?: 'Mutation';
  /** Добавление атрибута */
  addAttribute: AddAttributeMutationPayload;
  /** Добавление нового КБК */
  addBudgetClassification: AddBudgetClassificationMutationPayload;
  /** Мутация для добавления категории */
  addCategory: AddCategoryMutationPayload;
  /** Добавление дочерней строки. */
  addChildRowDimension: AddChildRowDimensionMutationPayload;
  /** Мутация на добавление дивизионов в период. */
  addDivisions: AddDivisionsMutationPayload;
  /** Мутация для добавления дивизионов из файла. */
  addDivisionsFromFile: AddDivisionsFromFileMutationPayload;
  /** Мутация для добавления дивизионов из других периодов. */
  addDivisionsFromPeriod: AddDivisionsFromPeriodMutationPayload;
  /** Добавление документа. */
  addDocument: AddDocumentMutationPayload;
  /** Загрузка данных из файла. */
  addDocumentData: AddDocumentDataMutationPayload;
  /** Добавление статуса документа. */
  addDocumentStatus: AddDocumentStatusMutationPayload;
  /** Мутация для загрузки файлов */
  addFile: AddFileMutationPayload;
  /** Мутация для добавления группы. */
  addGroup: AddGroupMutationPayload;
  /** Добавление страницы */
  addPage: AddPageMutationPayload;
  /** Мутация для создания периода. */
  addPeriod: AddPeriodMutationPayload;
  /** Мутация на добавление группы в период. */
  addPeriodGroup: AddPeriodGroupMutationPayload;
  /** Мутация для добавления записи профиля. */
  addProfile: AddProfileMutationPayload;
  /** Мутация для добавления проекта. */
  addProject: AddProjectMutationPayload;
  /** Добавление строки */
  addRowDimension: AddRowDimensionMutationPayload;
  /** Добавление секции */
  addSectionFiles: AddSectionFilesMutationPayload;
  /** Добавление секции */
  addSectionGallery: AddSectionGalleryMutationPayload;
  /** Добавление секции */
  addSectionText: AddSectionTextMutationPayload;
  /** Добавление тега */
  addTag: AddTagMutationPayload;
  /** Авторизация через портал https://cbias.ru */
  authCbias?: Maybe<AuthCbiasMutationOutput>;
  /** Изменение атрибута */
  changeAttribute: ChangeAttributeMutationPayload;
  /** Изменение значения */
  changeAttributeValue: ChangeAttributeValueMutationPayload;
  /** Мутация для изменения аватара пользователя. */
  changeAvatar: ChangeAvatarMutationPayload;
  /** Мутации для изменения категории */
  changeCategory: ChangeCategoryMutationPayload;
  /** Мутация для изменения аватара категории */
  changeCategoryAvatar: ChangeCategoryAvatarMutationPayload;
  /** Мутация для изменения родителя */
  changeCategoryParent: ChangeCategoryParentMutationPayload;
  /** Мутация для изменения порядка следования вывода категорий */
  changeCategoryPosition: ChangeCategoryPositionMutationPayload;
  /** Изменение значения ячейки по умолчанию */
  changeCellDefault: ChangeCellDefaultPayload;
  /** Изменения опций ячейки */
  changeCellsOption: ChangeCellsOptionMutationPayload;
  /** Изменение высоты дочерней строки. */
  changeChildRowDimensionHeight: ChangeChildRowDimensionHeightMutationPayload;
  /** Изменение колонки */
  changeColumnDimension: ChangeColumnDimensionMutationPayload;
  /** Изменение свойства fixed у колонок */
  changeColumnDimensionsFixed: ChangeColumnDimensionsFixedPayload;
  /** Изменение комментария версии документа. */
  changeDocumentComment: ChangeDocumentCommentMutationPayload;
  /** Мутация для изменения файла */
  changeFile: ChangeFileMutationPayload;
  /** Изменение значения ячейки типа `Файл` */
  changeFileValue: ChangeFileValueMutationPayload;
  /** Мутация для изменения имени группы. */
  changeGroupName: ChangeGroupNameMutationPayload;
  /** Мутация для изменения привилегий группы. */
  changeGroupPermissions: ChangeGroupPermissionsMutationPayload;
  /** Изменение свойств уведомления */
  changeNotification: ChangeNotificationMutationPayload;
  /** Изменение свойств уведомлений */
  changeNotifications: ChangeNotificationsMutationPayload;
  /** Изменение аватара на странице */
  changePageAvatar: ChangePageAvatarMutationPayload;
  /** Изменение boolean свойств страницы */
  changePageBooleanProperty: ChangePageBooleanPropertyMutationPayload;
  /** Изменение категории страницы */
  changePageCategory: ChangePageCategoryMutationPayload;
  /** Изменение типа страницы */
  changePageKind: ChangePageKindMutationPayload;
  /** Изменения тегов страницы */
  changePageTags: ChangePageTagsMutationPayload;
  /** Изменение названия страницы */
  changePageTitle: ChangePageTitleMutationPayload;
  /** Мутация для изменения пароля пользователя. */
  changePassword: ChangePasswordMutationPayload;
  /** Мутация на изменение настроек периода. */
  changePeriod: ChangePeriodMutationPayload;
  /** Мутация на изменение привилегий группы. */
  changePeriodGroupPrivileges: ChangePeriodGroupPrivilegesMutationPayload;
  /** Мутация на изменение значения профиля. */
  changeProfileValue: ChangeProfileValueMutationPayload;
  /** Матция для изменения видимости. */
  changeProfileVisibility: ChangeProfileVisibilityMutationPayload;
  /** Мутация изменения настроек проекта. */
  changeProject: ChangeProjectMutationPayload;
  /** Изменение строки */
  changeRowDimension: ChangeRowDimensionMutationPayload;
  /** Изменение свойства fixed у строк */
  changeRowDimensionsFixed: ChangeRowDimensionsFixedPayload;
  /** Изменение текста секции */
  changeSectionFiles: ChangeSectionFilesMutationPayload;
  /** Изменение текста секции */
  changeSectionGallery: ChangeSectionGalleryMutationPayload;
  /** Изменение текста секции */
  changeSectionText: ChangeSectionTextMutationPayload;
  /** Мутация для изменения настроек */
  changeSettings: ChangeSettingsMutationPayload;
  /** Показ листов */
  changeShowSheet: ChangeShowSheetMutationPayload;
  /** Мутация для изменения групп конкретного пользователя. */
  changeUserGroups: ChangeUserGroupsMutationPayload;
  /** Мутация на изменение групп пользователя в периоде. */
  changeUserPeriodGroups: ChangeUserPeriodGroupsMutationPayload;
  /** Мутация на изменение отдельных привилегий пользователя в периоде. */
  changeUserPeriodPrivileges: ChangeUserPeriodPrivilegesMutationPayload;
  /** Мутация для изменения полей пользователя. */
  changeUserProps: ChangeUserPropsMutationPayload;
  /** Изменение значения ячейки */
  changeValue: ChangeValueMutationPayload;
  /** Подтверждение кода. */
  confirmEmail: ConfirmEmailMutationPayload;
  /** Мутация на перенос групп с пользователями из другого периода. */
  copyPeriodGroups: CopyPeriodGroupsMutationPayload;
  /** Удаление атрибута */
  deleteAttribute: DeleteAttributeMutationPayload;
  /** Мутация для удаления категории */
  deleteCategory: DeleteCategoryMutationPayload;
  /** Удаление дочерней строки. */
  deleteChildRowDimension: DeleteChildRowDimensionMutationPayload;
  /** Мутация на удаление дивизиона из периода. */
  deleteDivision: DeleteDivisionMutationPayload;
  /** Удаление статуса документа. */
  deleteDocumentStatus: DeleteDocumentStatusMutationPayload;
  /** Мутация для полного удаления файла */
  deleteFile: DeleteFileMutationPayload;
  /** Мутация для удаления группы. */
  deleteGroup: DeleteGroupMutationPayload;
  /** Удаление уведомления */
  deleteNotice: DeleteNoticeMutationPayload;
  /** Удаление страницы */
  deletePage: DeletePageMutationPayload;
  /** Мутация на удаление периода. */
  deletePeriod: DeletePeriodMutationPayload;
  /** Мутация на удаление группы периода. */
  deletePeriodGroup: DeletePeriodGroupMutationPayload;
  /** Мутация для удаления записи профиля. */
  deleteProfile: DeleteProfileMutationPayload;
  /** Мутация на удаление проекта. */
  deleteProject: DeleteProjectMutationPayload;
  /** Удаление строки */
  deleteRowDimension: DeleteRowDimensionMutationPayload;
  /** Удаление секции */
  deleteSection: DeleteSectionMutationPayload;
  /** Мутация для удаления всех сессий кроме текущей. */
  deleteSessions: DeleteSessionsMutationPayload;
  /** Мутация для получения токена авторизации. */
  getToken: GetTokenMutationPayload;
  /** Мутация выхода */
  logout: LogoutMutationPayload;
  /** Мутация для сброса пароля пользователя. */
  recoveryPassword: RecoveryPasswordMutationPayload;
  /** Мутация регистрации новых пользователей. */
  register: RegisterMutationPayload;
  /** Изменение названия листа */
  renameSheet: RenameSheetMutationPayload;
  /** Отправка email с кодом на электронную почту. */
  requestCode: RequestCodeMutationPayload;
  /** Мутация для сброса настроек по умолчанию */
  resetSettings: ResetSettingsMutationPayload;
  /** Мутация для сброса пароля пользователя. */
  restorePassword: RestorePasswordMutationPayload;
  /** Отправка письма поддержки */
  supportSubmit: SupportSubmitMutationPayload;
  /** Выгрузка документа. */
  unloadDocument: UnloadDocumentMutationPayload;
  /** Выгрузка архива значения ячейки типа `Файл` */
  unloadFileValueArchive: UnloadFileValueArchiveMutationPayload;
  /** Мутация для загрузки пользователей из файла excel | csv. */
  uploadUsers: UploadUsersMutationPayload;
};

/** Мутации на изменение чего-либо. */
export type MutationAddAttributeArgs = {
  input: AddAttributeMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddBudgetClassificationArgs = {
  input: AddBudgetClassificationMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddCategoryArgs = {
  input: AddCategoryMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddChildRowDimensionArgs = {
  input: AddChildRowDimensionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddDivisionsArgs = {
  input: AddDivisionsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddDivisionsFromFileArgs = {
  input: AddDivisionsFromFileMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddDivisionsFromPeriodArgs = {
  input: AddDivisionsFromPeriodMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddDocumentArgs = {
  input: AddDocumentMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddDocumentDataArgs = {
  input: AddDocumentDataMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddDocumentStatusArgs = {
  input: AddDocumentStatusMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddFileArgs = {
  input: AddFileMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddGroupArgs = {
  input: AddGroupMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddPageArgs = {
  input: AddPageMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddPeriodArgs = {
  input: AddPeriodMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddPeriodGroupArgs = {
  input: AddPeriodGroupMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddProfileArgs = {
  input: AddProfileMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddProjectArgs = {
  input: AddProjectMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddRowDimensionArgs = {
  input: AddRowDimensionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddSectionFilesArgs = {
  input: AddSectionFilesMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddSectionGalleryArgs = {
  input: AddSectionGalleryMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddSectionTextArgs = {
  input: AddSectionTextMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAddTagArgs = {
  input: AddTagMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationAuthCbiasArgs = {
  payload: AuthCbiasMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeAttributeArgs = {
  input: ChangeAttributeMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeAttributeValueArgs = {
  input: ChangeAttributeValueMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeAvatarArgs = {
  input: ChangeAvatarMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeCategoryArgs = {
  input: ChangeCategoryMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeCategoryAvatarArgs = {
  input: ChangeCategoryAvatarMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeCategoryParentArgs = {
  input: ChangeCategoryParentMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeCategoryPositionArgs = {
  input: ChangeCategoryPositionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeCellDefaultArgs = {
  input: ChangeCellDefaultInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeCellsOptionArgs = {
  input: ChangeCellsOptionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeChildRowDimensionHeightArgs = {
  input: ChangeChildRowDimensionHeightMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeColumnDimensionArgs = {
  input: ChangeColumnDimensionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeColumnDimensionsFixedArgs = {
  input: ChangeColumnDimensionsFixedInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeDocumentCommentArgs = {
  input: ChangeDocumentCommentMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeFileArgs = {
  input: ChangeFileMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeFileValueArgs = {
  input: ChangeFileValueMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeGroupNameArgs = {
  input: ChangeGroupNameMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeGroupPermissionsArgs = {
  input: ChangeGroupPermissionsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeNotificationArgs = {
  input: ChangeNotificationMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeNotificationsArgs = {
  input: ChangeNotificationsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePageAvatarArgs = {
  input: ChangePageAvatarMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePageBooleanPropertyArgs = {
  input: ChangePageBooleanPropertyMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePageCategoryArgs = {
  input: ChangePageCategoryMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePageKindArgs = {
  input: ChangePageKindMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePageTagsArgs = {
  input: ChangePageTagsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePageTitleArgs = {
  input: ChangePageTitleMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePasswordArgs = {
  input: ChangePasswordMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePeriodArgs = {
  input: ChangePeriodMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangePeriodGroupPrivilegesArgs = {
  input: ChangePeriodGroupPrivilegesMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeProfileValueArgs = {
  input: ChangeProfileValueMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeProfileVisibilityArgs = {
  input: ChangeProfileVisibilityMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeProjectArgs = {
  input: ChangeProjectMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeRowDimensionArgs = {
  input: ChangeRowDimensionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeRowDimensionsFixedArgs = {
  input: ChangeRowDimensionsFixedInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeSectionFilesArgs = {
  input: ChangeSectionFilesMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeSectionGalleryArgs = {
  input: ChangeSectionGalleryMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeSectionTextArgs = {
  input: ChangeSectionTextMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeSettingsArgs = {
  input: ChangeSettingsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeShowSheetArgs = {
  input: ChangeShowSheetMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeUserGroupsArgs = {
  input: ChangeUserGroupsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeUserPeriodGroupsArgs = {
  input: ChangeUserPeriodGroupsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeUserPeriodPrivilegesArgs = {
  input: ChangeUserPeriodPrivilegesMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeUserPropsArgs = {
  input: ChangeUserPropsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationChangeValueArgs = {
  input: ChangeValueMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationConfirmEmailArgs = {
  input: ConfirmEmailMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationCopyPeriodGroupsArgs = {
  input: CopyPeriodGroupsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteAttributeArgs = {
  input: DeleteAttributeMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteCategoryArgs = {
  input: DeleteCategoryMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteChildRowDimensionArgs = {
  input: DeleteChildRowDimensionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteDivisionArgs = {
  input: DeleteDivisionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteDocumentStatusArgs = {
  input: DeleteDocumentStatusMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteFileArgs = {
  input: DeleteFileMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteGroupArgs = {
  input: DeleteGroupMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteNoticeArgs = {
  input: DeleteNoticeMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeletePageArgs = {
  input: DeletePageMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeletePeriodArgs = {
  input: DeletePeriodMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeletePeriodGroupArgs = {
  input: DeletePeriodGroupMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteProfileArgs = {
  input: DeleteProfileMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteProjectArgs = {
  input: DeleteProjectMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteRowDimensionArgs = {
  input: DeleteRowDimensionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteSectionArgs = {
  input: DeleteSectionMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationDeleteSessionsArgs = {
  input: DeleteSessionsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationGetTokenArgs = {
  input: GetTokenMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationLogoutArgs = {
  input: LogoutMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationRecoveryPasswordArgs = {
  input: RecoveryPasswordMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationRegisterArgs = {
  input: RegisterMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationRenameSheetArgs = {
  input: RenameSheetMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationRequestCodeArgs = {
  input: RequestCodeMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationResetSettingsArgs = {
  input: ResetSettingsMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationRestorePasswordArgs = {
  input: RestorePasswordMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationSupportSubmitArgs = {
  input: SupportSubmitMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationUnloadDocumentArgs = {
  input: UnloadDocumentMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationUnloadFileValueArchiveArgs = {
  input: UnloadFileValueArchiveMutationInput;
};

/** Мутации на изменение чего-либо. */
export type MutationUploadUsersArgs = {
  input: UploadUsersMutationInput;
};

/** An object with an ID */
export type Node = {
  /** The ID of the object. */
  id: Scalars['ID'];
};

/** Уведомление без дополнительного содержимого */
export type NoticeEmptyType = NoticeInterface & {
  __typename?: 'NoticeEmptyType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Тип уведомления */
  kind: Scalars['Int'];
  /** Идентификатор объекта */
  objectId: Scalars['String'];
  /** Полезная нагрузка */
  payload: Scalars['String'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

/** Переопределение стандартного интерфейса уведомлений. */
export type NoticeInterface = {
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Тип уведомления */
  kind: Scalars['Int'];
  /** Идентификатор объекта */
  objectId: Scalars['String'];
  /** Полезная нагрузка */
  payload: Scalars['String'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

/** An enumeration. */
export type NoticeKind =
  /** info */
  | 'A_0'
  /** page */
  | 'A_1'
  /** comment */
  | 'A_2'
  /** message */
  | 'A_3'
  /** task */
  | 'A_4'
  /** billing */
  | 'A_5'
  /** paid */
  | 'A_6'
  /** mailing */
  | 'A_7'
  /** happy_birthday */
  | 'A_8';

/** Уведомление типа 'Пришло уведомление'. */
export type NoticeMailingType = NoticeInterface & {
  __typename?: 'NoticeMailingType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Тип уведомления */
  kind: Scalars['Int'];
  /** Оповещение пользователя */
  mailing?: Maybe<MailingType>;
  /** Идентификатор объекта */
  objectId: Scalars['String'];
  /** Полезная нагрузка */
  payload: Scalars['String'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

/** Уведомление типа 'Добавлена новая страница' */
export type NoticePageType = NoticeInterface & {
  __typename?: 'NoticePageType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Тип уведомления */
  kind: Scalars['Int'];
  /** Идентификатор объекта */
  objectId: Scalars['String'];
  /** Страница */
  page?: Maybe<PageType>;
  /** Полезная нагрузка */
  payload: Scalars['String'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

/** Уведомление */
export type NoticeType = Node & {
  __typename?: 'NoticeType';
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Тип уведомления */
  kind: NoticeKind;
  /** Идентификатор объекта */
  objectId: Scalars['String'];
  /** Полезная нагрузка */
  payload: Scalars['String'];
  /** Пользователь */
  user?: Maybe<UserType>;
};

export type NoticeTypeConnection = {
  __typename?: 'NoticeTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<NoticeTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `NoticeType` and its cursor. */
export type NoticeTypeEdge = {
  __typename?: 'NoticeTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<NoticeType>;
};

/** Оповещение пользователей */
export type NotificationType = Node & {
  __typename?: 'NotificationType';
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** Скрыть уведомление */
  hide: Scalars['Boolean'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Уведомление */
  notice: NoticeInterface;
  /** Прочитано ли уведомление */
  read: Scalars['Boolean'];
  /** Пользователь */
  user: UserType;
};

export type NotificationTypeConnection = {
  __typename?: 'NotificationTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<NotificationTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `NotificationType` and its cursor. */
export type NotificationTypeEdge = {
  __typename?: 'NotificationTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<NotificationType>;
};

/** Подписка на обновление событий. */
export type NotificationsSubscription = {
  __typename?: 'NotificationsSubscription';
  /** Действие пользователя */
  action: ConsumerActionType;
  /** Идентификатор объекта */
  id: Scalars['ID'];
  notification?: Maybe<NotificationType>;
};

export type OrganizationAddressFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationDepartmentFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Array<InputMaybe<Scalars['ID']>>>;
  /** `In` lookup */
  in?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

export type OrganizationFilterInputType = {
  /** `Address` field */
  address?: InputMaybe<OrganizationAddressFilterInputType>;
  /** `And` field */
  and?: InputMaybe<Array<InputMaybe<OrganizationFilterInputType>>>;
  /** `Department` field */
  department?: InputMaybe<OrganizationDepartmentFilterInputType>;
  /** `Id` field */
  id?: InputMaybe<OrganizationIdFilterInputType>;
  /** `Inn` field */
  inn?: InputMaybe<OrganizationInnFilterInputType>;
  /** `Kind` field */
  kind?: InputMaybe<OrganizationKindFilterInputType>;
  /** `Kodbuhg` field */
  kodbuhg?: InputMaybe<OrganizationKodbuhgFilterInputType>;
  /** `Kpp` field */
  kpp?: InputMaybe<OrganizationKppFilterInputType>;
  /** `Mail` field */
  mail?: InputMaybe<OrganizationMailFilterInputType>;
  /** `Name` field */
  name?: InputMaybe<OrganizationNameFilterInputType>;
  /** `Not` field */
  not?: InputMaybe<OrganizationFilterInputType>;
  /** `Okpo` field */
  okpo?: InputMaybe<OrganizationOkpoFilterInputType>;
  /** `Or` field */
  or?: InputMaybe<Array<InputMaybe<OrganizationFilterInputType>>>;
  /** `Parent` field */
  parent?: InputMaybe<OrganizationParentFilterInputType>;
  /** `Phone` field */
  phone?: InputMaybe<OrganizationPhoneFilterInputType>;
  /** `Region` field */
  region?: InputMaybe<OrganizationRegionFilterInputType>;
  /** `Rubpnubp` field */
  rubpnubp?: InputMaybe<OrganizationRubpnubpFilterInputType>;
  /** `Site` field */
  site?: InputMaybe<OrganizationSiteFilterInputType>;
};

export type OrganizationIdFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['ID']>;
  /** `In` lookup */
  in?: InputMaybe<Array<InputMaybe<Scalars['String']>>>;
};

export type OrganizationInnFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationKindFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationKodbuhgFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationKppFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationMailFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationNameFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationOkpoFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

/** Описание списка организаций. */
export type OrganizationOriginalType = {
  __typename?: 'OrganizationOriginalType';
  /** Address */
  address?: Maybe<Scalars['String']>;
  /** Additional fields */
  attributes: Scalars['JSONString'];
  /** Created date */
  createdAt: Scalars['DateTime'];
  /** Департаменты */
  departments?: Maybe<Array<Maybe<DepartmentType>>>;
  id: Scalars['ID'];
  /** Individual taxpayer number */
  inn?: Maybe<Scalars['String']>;
  /** Type */
  kind?: Maybe<Scalars['String']>;
  /** Accounting code */
  kodbuhg?: Maybe<Scalars['String']>;
  /** Code of reason */
  kpp?: Maybe<Scalars['String']>;
  /** Email */
  mail?: Maybe<Scalars['String']>;
  /** Name */
  name: Scalars['String'];
  /** Russian classifier of enterprises and organizations */
  okpo?: Maybe<Scalars['String']>;
  /** Parent */
  parent?: Maybe<OrganizationOriginalType>;
  /** Phone number */
  phone?: Maybe<Scalars['String']>;
  /** Name for view */
  presentName: Scalars['String'];
  /** Region */
  region?: Maybe<RegionType>;
  /** Rubpnubp code */
  rubpnubp?: Maybe<Scalars['String']>;
  /** Site url */
  site?: Maybe<Scalars['String']>;
  /** Updated date */
  updatedAt: Scalars['DateTime'];
  /** Пользователи */
  users?: Maybe<Array<Maybe<UserType>>>;
};

export type OrganizationParentFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['ID']>;
  /** `Isnull` lookup */
  isnull?: InputMaybe<Scalars['Boolean']>;
};

export type OrganizationPhoneFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationRegionFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['ID']>;
  /** `In` lookup */
  in?: InputMaybe<Array<InputMaybe<Scalars['ID']>>>;
};

export type OrganizationRubpnubpFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

export type OrganizationSiteFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['String']>;
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

/** Optimized type for Organizations. */
export type OrganizationType = Node & {
  __typename?: 'OrganizationType';
  /** Address */
  address?: Maybe<Scalars['String']>;
  /** Additional fields */
  attributes: Scalars['JSONString'];
  /** Children of organization */
  children?: Maybe<Array<Maybe<OrganizationType>>>;
  /** Created date */
  createdAt: Scalars['DateTime'];
  /** Departments. */
  departments?: Maybe<Array<Maybe<DepartmentType>>>;
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Individual taxpayer number */
  inn?: Maybe<Scalars['String']>;
  /** Type */
  kind?: Maybe<Scalars['String']>;
  /** Accounting code */
  kodbuhg?: Maybe<Scalars['String']>;
  /** Code of reason */
  kpp?: Maybe<Scalars['String']>;
  /** Email */
  mail?: Maybe<Scalars['String']>;
  /** Name */
  name: Scalars['String'];
  /** Russian classifier of enterprises and organizations */
  okpo?: Maybe<Scalars['String']>;
  /** Parent */
  parent?: Maybe<OrganizationOriginalType>;
  /** Phone number */
  phone?: Maybe<Scalars['String']>;
  /** Name for view */
  presentName: Scalars['String'];
  /** Region */
  region?: Maybe<RegionType>;
  /** Rubpnubp code */
  rubpnubp?: Maybe<Scalars['String']>;
  /** Site url */
  site?: Maybe<Scalars['String']>;
  /** Updated date */
  updatedAt: Scalars['DateTime'];
};

export type OrganizationTypeConnection = {
  __typename?: 'OrganizationTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<OrganizationTypeEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `OrganizationType` and its cursor. */
export type OrganizationTypeEdge = {
  __typename?: 'OrganizationTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<OrganizationType>;
};

/** The Relay compliant `PageInfo` type, containing data necessary to paginate this connection. */
export type PageInfo = {
  __typename?: 'PageInfo';
  /** When paginating forwards, the cursor to continue. */
  endCursor?: Maybe<Scalars['String']>;
  /** When paginating forwards, are there more items? */
  hasNextPage: Scalars['Boolean'];
  /** When paginating backwards, are there more items? */
  hasPreviousPage: Scalars['Boolean'];
  /** When paginating backwards, the cursor to continue. */
  startCursor?: Maybe<Scalars['String']>;
};

/** Тип страницы */
export type PageKindType = {
  __typename?: 'PageKindType';
  id: Scalars['ID'];
  /** Название */
  name: Scalars['String'];
  /** Странички */
  pages: Array<Maybe<PageType>>;
  /** Сегментные элементы */
  segmentElements: Array<Maybe<SegmentElementType>>;
};

/** Страница */
export type PageType = Node & {
  __typename?: 'PageType';
  /** Аватар */
  avatar?: Maybe<Scalars['String']>;
  /** Категория */
  category: CategoryType;
  /** Комментарии */
  comments: CommentTypeConnection;
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** Скрываем ли страницу */
  hide: Scalars['Boolean'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Тип */
  kind?: Maybe<PageKindType>;
  /** Показывать параллакс или нет */
  parallax: Scalars['Boolean'];
  /** Первая текстовая секция */
  preview?: Maybe<Scalars['String']>;
  /** Приоритет */
  priority: Scalars['Boolean'];
  /** Секции */
  sections: Array<Maybe<SectionInterface>>;
  /** Подпись страницы */
  signature?: Maybe<Scalars['String']>;
  /** Теги на странице */
  tags: Array<Maybe<TagType>>;
  /** Заголовок */
  title: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь, создавший страницу */
  user?: Maybe<UserType>;
  /** Количество просмотров */
  views: Scalars['Int'];
};

/** Страница */
export type PageTypeCommentsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  text_Icontains?: InputMaybe<Scalars['String']>;
};

export type PageTypeConnection = {
  __typename?: 'PageTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<PageTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `PageType` and its cursor. */
export type PageTypeEdge = {
  __typename?: 'PageTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<PageType>;
};

/** Группы с содержанием привилегий. */
export type PeriodGroupType = {
  __typename?: 'PeriodGroupType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  id: Scalars['ID'];
  /** Наименование группы периода привилегии */
  name: Scalars['String'];
  /** Период сбора */
  period: PeriodType;
  /** Привилегии группы */
  privileges?: Maybe<Array<PrivilegeType>>;
  /** Пользователи в группе */
  users?: Maybe<Array<UserType>>;
};

/** Тип периода. */
export type PeriodType = {
  __typename?: 'PeriodType';
  /** Может ли пользователь добавлять документы в период */
  canAddDocument: Scalars['Boolean'];
  /** Может ли пользователь изменять дивизионы периода */
  canChangeDivisions: Scalars['Boolean'];
  /** Может ли пользователь изменять группы периода */
  canChangeGroups: Scalars['Boolean'];
  /** Может ли пользователь изменять настройки периода */
  canChangeSettings: Scalars['Boolean'];
  /** Может ли пользователь изменять структуру листа периода */
  canChangeSheet: Scalars['Boolean'];
  /** Может ли пользователь изменять пользователей периода */
  canChangeUsers: Scalars['Boolean'];
  /** Может ли пользователь удалять период */
  canDelete: Scalars['Boolean'];
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** Участвующие дивизионы */
  divisions?: Maybe<Array<Maybe<DivisionModelType>>>;
  /** Дата окончания */
  expiration?: Maybe<Scalars['Date']>;
  id: Scalars['ID'];
  /** Методическая поддержка */
  methodicalSupport?: Maybe<Array<FileType>>;
  /** Множественное заполнение */
  multiple: Scalars['Boolean'];
  /** Наименование периода */
  name: Scalars['String'];
  /** Группы пользователей назначенных в сборе */
  periodGroups?: Maybe<Array<Maybe<PeriodGroupType>>>;
  /** Приватность полей */
  privately: Scalars['Boolean'];
  /** Проект */
  project?: Maybe<ProjectType>;
  /** Листы */
  sheets: Array<Maybe<BaseSheetType>>;
  /** Дата начала */
  start?: Maybe<Scalars['Date']>;
  /** Статус проекта */
  status: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь */
  user: UserType;
  /** Множество версий */
  versioning: Scalars['Boolean'];
};

/** Привилегия пользователя или группы пользователей. */
export type PermissionType = {
  __typename?: 'PermissionType';
  codename: Scalars['String'];
  /** Тип модели Django */
  contentType: ContentTypeType;
  /** Группы */
  groups?: Maybe<GroupType>;
  id: Scalars['ID'];
  name: Scalars['String'];
};

/** Информация по показателям для типов различных показателей. */
export type PointStatisticsType = {
  __typename?: 'PointStatisticsType';
  /** Название */
  name: Scalars['String'];
  /** Текущее значение */
  value: Scalars['Int'];
};

/** Описание сквозных привилегий. */
export type PrivilegeType = {
  __typename?: 'PrivilegeType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  id: Scalars['ID'];
  /** Ключ привилегии */
  key: Scalars['String'];
  /** Наименование привилегии */
  name: Scalars['String'];
};

/** An enumeration. */
export type ProfileKind =
  /** text */
  | 'A_0'
  /** date */
  | 'A_1'
  /** bool */
  | 'A_2'
  /** file */
  | 'A_3'
  /** choice */
  | 'A_4';

/** Тип параметров пользователей. */
export type ProfileType = {
  __typename?: 'ProfileType';
  /** Доступные дочерние поля */
  available: Array<ProfileType>;
  /** Дочерние */
  children: Array<ProfileType>;
  /** Уникальный код настройки */
  code: Scalars['String'];
  id: Scalars['ID'];
  /** Тип настройки */
  kind: ProfileKind;
  /** Название настройки */
  name: Scalars['String'];
  /** Позиция */
  position: Scalars['Int'];
  /** Значение пользователя */
  value?: Maybe<ProfileValueType>;
};

/** Значение параметров пользователей. */
export type ProfileValueType = {
  __typename?: 'ProfileValueType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  id: Scalars['ID'];
  /** Профиль */
  profile: ProfileType;
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь */
  user: UserType;
  /** Значение хранимой информации */
  value: Scalars['String'];
  /** Доступность настройки */
  visibility: Scalars['Boolean'];
};

export type ProjectFilterInputType = {
  /** `And` field */
  and?: InputMaybe<Array<InputMaybe<ProjectFilterInputType>>>;
  /** `Name` field */
  name?: InputMaybe<ProjectNameFilterInputType>;
  /** `Not` field */
  not?: InputMaybe<ProjectFilterInputType>;
  /** `Or` field */
  or?: InputMaybe<Array<InputMaybe<ProjectFilterInputType>>>;
  /** `User` field */
  user?: InputMaybe<ProjectUserFilterInputType>;
};

export type ProjectNameFilterInputType = {
  /** `Icontains` lookup */
  icontains?: InputMaybe<Scalars['String']>;
};

/** Тип модели проектов. */
export type ProjectType = Node & {
  __typename?: 'ProjectType';
  /** Архив */
  archive: Scalars['Boolean'];
  /** Может ли пользователь добавлять периоды в проект */
  canAddPeriod: Scalars['Boolean'];
  /** Может ли пользователь изменять проект */
  canChange: Scalars['Boolean'];
  /** Может ли пользователь удалять проект */
  canDelete: Scalars['Boolean'];
  /** Дивизион: Department, Organizations */
  contentType: ContentTypeType;
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** Описание проекта */
  description: Scalars['String'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Наименование проекта */
  name: Scalars['String'];
  /** Периоды */
  periods?: Maybe<Array<Maybe<PeriodType>>>;
  /** Сокращенное наименование проекта */
  short: Scalars['String'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь */
  user?: Maybe<UserType>;
  /** Видимость проекта */
  visibility: Scalars['Boolean'];
};

export type ProjectTypeConnection = {
  __typename?: 'ProjectTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<ProjectTypeEdge>>;
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `ProjectType` and its cursor. */
export type ProjectTypeEdge = {
  __typename?: 'ProjectTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<ProjectType>;
};

export type ProjectUserFilterInputType = {
  /** `Exact` lookup */
  exact?: InputMaybe<Scalars['ID']>;
  /** `In` lookup */
  in?: InputMaybe<Array<InputMaybe<Scalars['ID']>>>;
};

/** Схема запросов данных. */
export type Query = {
  __typename?: 'Query';
  _debug?: Maybe<DjangoDebug>;
  activeBudgetClassifications?: Maybe<BudgetClassificationTypeConnection>;
  /** Статистика активности */
  activeStatistics: ActiveStatisticsType;
  /** Приложения */
  applications: Array<ApplicationType>;
  /** Получение атрибутов, привязанных к периоду */
  attributes: Array<Maybe<AttributeType>>;
  /** Атрибуты со значениями документа */
  attributesValues: Array<Maybe<AttributeValueType>>;
  budgetClassifications?: Maybe<BudgetClassificationTypeConnection>;
  /** Категории */
  categories: CategoryTypeConnection;
  /** Категория */
  category: CategoryType;
  department?: Maybe<DepartmentType>;
  departments?: Maybe<Array<DepartmentType>>;
  district?: Maybe<DistrictType>;
  districts?: Maybe<Array<DistrictType>>;
  /** Документ */
  document?: Maybe<DocumentType>;
  /** Выгрузка листа с несколькими документами */
  documentSheet: SheetType;
  /** Статусы документов */
  documentStatuses?: Maybe<Array<DocumentStatusType>>;
  /** Документы */
  documents: DocumentTypeConnection;
  /** Выгрузка листа с несколькими документами */
  documentsSheet: SheetType;
  files: FileTypeConnection;
  groups: Array<GroupType>;
  /** Установлены ли настройки приложения */
  hasSettings: Scalars['Boolean'];
  logEntry: LogEntryTypeConnection;
  logRequests: LogRequestTypeConnection;
  /** Информация обо мне */
  me?: Maybe<UserType>;
  /** Источник уведомлений */
  notices: NoticeTypeConnection;
  /** Детализация уведомления */
  notification: NotificationType;
  /** Уведомления пользователя */
  notifications: NotificationTypeConnection;
  organization?: Maybe<OrganizationType>;
  organizations?: Maybe<OrganizationTypeConnection>;
  /** Страница */
  page: PageType;
  /** Получение типа страницы */
  pageKind: PageKindType;
  /** Типы страниц */
  pageKinds: Array<PageKindType>;
  /** Страницы */
  pages: PageTypeConnection;
  /** Период */
  period: PeriodType;
  /** Возможные дивизионы периода */
  periodPossibleDivisions?: Maybe<DivisionModelTypeConnection>;
  /** Пользователи, связанные периодом */
  periodUsers: Array<UserType>;
  /** Периоды */
  periods: Array<PeriodType>;
  permissions: Array<PermissionType>;
  /** Привилегии */
  privileges: Array<PrivilegeType>;
  /** Доступные значения профиля пользователя */
  profileInformation: Array<ProfileType>;
  /** Список настроек профиля */
  profiles: Array<ProfileType>;
  /** Значение профиля пользователя */
  profilesValue: Array<ProfileValueType>;
  /** Проект */
  project: ProjectType;
  /** Проекты */
  projects?: Maybe<ProjectTypeConnection>;
  region?: Maybe<RegionType>;
  regions?: Maybe<Array<RegionType>>;
  /** Статистика запросов */
  requestStatistics: RequestStatisticsType;
  /** Сегменты страницы */
  segments: Array<SegmentType>;
  /** Доступные сессии */
  sessions: Array<SessionType>;
  /** Настройки приложения */
  settings: Array<SettingType>;
  /** Статусы */
  statuses?: Maybe<Array<StatusType>>;
  /** Теги */
  tags: TagTypeConnection;
  /** Информация о указанном пользователе */
  user?: Maybe<UserType>;
  /** Привилегии пользователя в группе периода */
  userGroupPrivileges: Array<PrivilegeType>;
  /** Доступная информация о пользователе */
  userInformation?: Maybe<UserType>;
  /** Отдельные привилегии пользователя для периода */
  userPeriodPrivileges: Array<PrivilegeType>;
  /** Пользователи приложения */
  users: UserTypeConnection;
  /** Файлы значения ячейки типа `Файл` */
  valueFiles?: Maybe<Array<FileType>>;
};

/** Схема запросов данных. */
export type QueryActiveBudgetClassificationsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  filter?: InputMaybe<ActiveBudgetClassificationFilterInputType>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
};

/** Схема запросов данных. */
export type QueryAttributesArgs = {
  parent?: InputMaybe<Scalars['Boolean']>;
  periodId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryAttributesValuesArgs = {
  documentId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryBudgetClassificationsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  filter?: InputMaybe<BudgetClassificationFilterInputType>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
};

/** Схема запросов данных. */
export type QueryCategoriesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  parent?: InputMaybe<Scalars['ID']>;
  parent_Isnull?: InputMaybe<Scalars['Boolean']>;
  text_Icontains?: InputMaybe<Scalars['String']>;
};

/** Схема запросов данных. */
export type QueryCategoryArgs = {
  categoryId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryDepartmentArgs = {
  departmentId: Scalars['Int'];
};

/** Схема запросов данных. */
export type QueryDistrictArgs = {
  districtId: Scalars['Int'];
};

/** Схема запросов данных. */
export type QueryDocumentArgs = {
  documentId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryDocumentSheetArgs = {
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryDocumentStatusesArgs = {
  documentId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryDocumentsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  divisionId_In?: InputMaybe<Array<InputMaybe<Scalars['ID']>>>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  lastStatus_StatusId_In?: InputMaybe<Array<InputMaybe<Scalars['ID']>>>;
  offset?: InputMaybe<Scalars['Int']>;
  periodId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryDocumentsSheetArgs = {
  documentIds?: InputMaybe<Array<Scalars['ID']>>;
  sheetId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryFilesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  name_Icontains?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
  userId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryLogEntryArgs = {
  action_Contains?: InputMaybe<Scalars['String']>;
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  contentType_Model_Icontains?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  objectId_Icontains?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  userId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryLogRequestsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  createdAt_Gt?: InputMaybe<Scalars['DateTime']>;
  createdAt_Gte?: InputMaybe<Scalars['DateTime']>;
  createdAt_Lt?: InputMaybe<Scalars['DateTime']>;
  createdAt_Lte?: InputMaybe<Scalars['DateTime']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  page_Icontains?: InputMaybe<Scalars['String']>;
  userId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryNoticesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  user?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryNotificationArgs = {
  notificationId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryNotificationsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  hide?: InputMaybe<Scalars['Boolean']>;
  last?: InputMaybe<Scalars['Int']>;
  notice?: InputMaybe<Scalars['ID']>;
  offset?: InputMaybe<Scalars['Int']>;
  user?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryOrganizationArgs = {
  organizationId: Scalars['Int'];
};

/** Схема запросов данных. */
export type QueryOrganizationsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  filter?: InputMaybe<OrganizationFilterInputType>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
};

/** Схема запросов данных. */
export type QueryPageArgs = {
  pageId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryPageKindArgs = {
  pageKindId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryPagesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  category_Id?: InputMaybe<Scalars['ID']>;
  first?: InputMaybe<Scalars['Int']>;
  kind_Id?: InputMaybe<Scalars['ID']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  title_Icontains?: InputMaybe<Scalars['String']>;
};

/** Схема запросов данных. */
export type QueryPeriodArgs = {
  periodId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryPeriodPossibleDivisionsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  periodId: Scalars['ID'];
  search?: InputMaybe<Scalars['String']>;
};

/** Схема запросов данных. */
export type QueryPeriodUsersArgs = {
  periodId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryPeriodsArgs = {
  projectId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryProfileInformationArgs = {
  userId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryProfilesValueArgs = {
  userId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryProjectArgs = {
  projectId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryProjectsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  filter?: InputMaybe<ProjectFilterInputType>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
};

/** Схема запросов данных. */
export type QueryRegionArgs = {
  regionId: Scalars['Int'];
};

/** Схема запросов данных. */
export type QuerySessionsArgs = {
  userId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryTagsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  name_Icontains?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
};

/** Схема запросов данных. */
export type QueryUserArgs = {
  userId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryUserGroupPrivilegesArgs = {
  periodGroupId: Scalars['ID'];
  userId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryUserInformationArgs = {
  userId: Scalars['ID'];
};

/** Схема запросов данных. */
export type QueryUserPeriodPrivilegesArgs = {
  periodId: Scalars['ID'];
  userId?: InputMaybe<Scalars['ID']>;
};

/** Схема запросов данных. */
export type QueryUsersArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  email_Icontains?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  firstName_Icontains?: InputMaybe<Scalars['String']>;
  last?: InputMaybe<Scalars['Int']>;
  lastName_Icontains?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
  sirName_Icontains?: InputMaybe<Scalars['String']>;
  username_Icontains?: InputMaybe<Scalars['String']>;
};

/** Схема запросов данных. */
export type QueryValueFilesArgs = {
  columnId: Scalars['ID'];
  documentId: Scalars['ID'];
  rowId: Scalars['ID'];
  sheetId: Scalars['ID'];
};

export type RecoveryPasswordMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Email адрес */
  email: Scalars['String'];
};

/** Мутация для сброса пароля пользователя. */
export type RecoveryPasswordMutationPayload = {
  __typename?: 'RecoveryPasswordMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Graphene object type for Regions. */
export type RegionType = {
  __typename?: 'RegionType';
  /** Real code of region */
  commonId?: Maybe<Scalars['Int']>;
  /** Created date */
  createdAt: Scalars['DateTime'];
  district?: Maybe<DistrictType>;
  id: Scalars['ID'];
  /** Region name */
  name: Scalars['String'];
  /** Updated date */
  updatedAt: Scalars['DateTime'];
};

export type RegisterMutationInput = {
  /** Согласие на обработку персональных данных */
  agreement: Scalars['Boolean'];
  /** Дата рождения */
  birthday: Scalars['Date'];
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Email */
  email: Scalars['String'];
  /** Имя */
  firstName: Scalars['String'];
  /** Фамилия */
  lastName: Scalars['String'];
  /** Пароль */
  password: Scalars['String'];
  /** Отчество */
  sirName?: InputMaybe<Scalars['String']>;
  /** Логин */
  username: Scalars['String'];
};

/** Мутация регистрации новых пользователей. */
export type RegisterMutationPayload = {
  __typename?: 'RegisterMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type RenameSheetMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Новое название листа */
  name: Scalars['String'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
};

/**
 * Изменение названия листа.
 *
 * Во время мутации изменяем только формулы и ничего не пересчитываем.
 */
export type RenameSheetMutationPayload = {
  __typename?: 'RenameSheetMutationPayload';
  /** Измененные ячейки */
  cells?: Maybe<Array<Maybe<CellType>>>;
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Лист */
  sheet?: Maybe<SheetType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type RequestCodeMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Email адрес */
  email: Scalars['String'];
};

/** Отправка email с кодом на электронную почту. */
export type RequestCodeMutationPayload = {
  __typename?: 'RequestCodeMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Информация по клиентам, с которых делаются запросы. */
export type RequestStatisticsType = {
  __typename?: 'RequestStatisticsType';
  /** Клиенты */
  browsers: Array<Maybe<PointStatisticsType>>;
  /** Устройства */
  device: Array<Maybe<PointStatisticsType>>;
  /** Операционные системы */
  os: Array<Maybe<PointStatisticsType>>;
};

export type ResetSettingsMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор пользователя */
  userId: Scalars['ID'];
};

/** Мутация для сброса настроек по умолчанию */
export type ResetSettingsMutationPayload = {
  __typename?: 'ResetSettingsMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Лист настроек */
  settings?: Maybe<Array<SettingType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type RestorePasswordMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Пароль */
  password: Scalars['String'];
  /** Токен */
  token: Scalars['String'];
};

/** Мутация для сброса пароля пользователя. */
export type RestorePasswordMutationPayload = {
  __typename?: 'RestorePasswordMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Тип строки. */
export type RowDimensionType = {
  __typename?: 'RowDimensionType';
  /** Агрегирование перечисление (мин, макс) для динамических строк */
  aggregation?: Maybe<Scalars['String']>;
  /** Ячейки */
  cells: Array<CellType>;
  /** Дочерние строки */
  children: Array<RowDimensionType>;
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** Идентификатор документа */
  documentId?: Maybe<Scalars['ID']>;
  /** Динамическая ли строка */
  dynamic: Scalars['Boolean'];
  /** Фиксация строки */
  fixed: Scalars['Boolean'];
  /** Индекс строки в плоской структуре */
  globalIndex: Scalars['Int'];
  /** Высота строки */
  height?: Maybe<Scalars['Int']>;
  /** Скрытие строки */
  hidden: Scalars['Boolean'];
  /** Идентификатор */
  id: Scalars['ID'];
  /** Индекс строки относительно родителя */
  index: Scalars['Int'];
  /** Название строки */
  name: Scalars['String'];
  /** Идентификатор дивизиона */
  objectId?: Maybe<Scalars['ID']>;
  /** Родительская строка */
  parent?: Maybe<RowDimensionType>;
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Идентификатор пользователя */
  userId?: Maybe<Scalars['ID']>;
};

/** Ошибка в строке. */
export type RowFieldErrorType = {
  __typename?: 'RowFieldErrorType';
  /** Ошибки, возникающие в строке */
  errors: Array<Maybe<ErrorFieldType>>;
  /** Номер строки с ошибкой */
  row: Scalars['Int'];
};

export type SectionFilesType = SectionInterface & {
  __typename?: 'SectionFilesType';
  /** Файлы */
  files: Array<Maybe<FileType>>;
  /** Идентификатор */
  id: Scalars['Int'];
  /** Тип страницы */
  kind: Scalars['Int'];
  /** Страница */
  page: PageType;
  /** Конструкции */
  payload?: Maybe<Scalars['JSONString']>;
  /** Порядок вывода */
  position: Scalars['Int'];
  /** Текст страницы */
  text: Scalars['String'];
  /** Пользователь */
  user: UserType;
};

export type SectionGalleryType = SectionInterface & {
  __typename?: 'SectionGalleryType';
  /** Идентификатор */
  id: Scalars['Int'];
  /** Изображения */
  images: Array<Maybe<FileType>>;
  /** Тип страницы */
  kind: Scalars['Int'];
  /** Страница */
  page: PageType;
  /** Конструкции */
  payload?: Maybe<Scalars['JSONString']>;
  /** Порядок вывода */
  position: Scalars['Int'];
  /** Текст страницы */
  text: Scalars['String'];
  /** Пользователь */
  user: UserType;
};

export type SectionInterface = {
  /** Идентификатор */
  id: Scalars['Int'];
  /** Тип страницы */
  kind: Scalars['Int'];
  /** Страница */
  page: PageType;
  /** Порядок вывода */
  position: Scalars['Int'];
  /** Текст страницы */
  text: Scalars['String'];
  /** Пользователь */
  user: UserType;
};

/** Секции */
export type SectionTextType = SectionInterface & {
  __typename?: 'SectionTextType';
  /** Идентификатор */
  id: Scalars['Int'];
  /** Тип страницы */
  kind: Scalars['Int'];
  /** Страница */
  page: PageType;
  /** Порядок вывода */
  position: Scalars['Int'];
  /** Текст страницы */
  text: Scalars['String'];
  /** Пользователь */
  user: UserType;
};

export type SectionUsersType = SectionInterface & {
  __typename?: 'SectionUsersType';
  /** Идентификатор */
  id: Scalars['Int'];
  /** Тип страницы */
  kind: Scalars['Int'];
  /** Страница */
  page: PageType;
  /** Конструкции */
  payload?: Maybe<Scalars['JSONString']>;
  /** Порядок вывода */
  position: Scalars['Int'];
  /** Текст страницы */
  text: Scalars['String'];
  /** Пользователь */
  user: UserType;
  /** Пользователи */
  users: Array<Maybe<UserType>>;
};

/** An enumeration. */
export type SegmentAlign =
  /** Left */
  | 'A_0'
  /** Center */
  | 'A_1'
  /** Right */
  | 'A_2';

/** An enumeration. */
export type SegmentElementRepresent =
  /** grid */
  | 'A_0'
  /** card */
  | 'A_1'
  /** list */
  | 'A_2'
  /** slider */
  | 'A_3';

/** Элемент сегмента */
export type SegmentElementType = {
  __typename?: 'SegmentElementType';
  /** Колонок в элементе */
  columns: Scalars['Int'];
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  id: Scalars['ID'];
  /** Тип страницы */
  pageKind: PageKindType;
  /** Количество страниц в запросе */
  pageSize: Scalars['Int'];
  /** Позиция в сортировке */
  position: Scalars['Int'];
  /** Представление */
  represent?: Maybe<SegmentElementRepresent>;
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Пользователь */
  user: UserType;
  /** Тип элемента для рендера */
  view?: Maybe<SegmentElementView>;
  /** Ширина колонки */
  width: Scalars['Int'];
};

/** An enumeration. */
export type SegmentElementView =
  /** empty */
  | 'A_0'
  /** card */
  | 'A_1';

/** Сегмент */
export type SegmentType = {
  __typename?: 'SegmentType';
  /** Выравнивание заголовка */
  align: SegmentAlign;
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** Элементы сегмента страницы */
  elements: Array<Maybe<SegmentElementType>>;
  id: Scalars['ID'];
  /** Заголовок страницы */
  name?: Maybe<Scalars['String']>;
  /** Позиция в сортировке */
  position: Scalars['Int'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
  /** Тип элемента для рендера */
  view?: Maybe<SegmentView>;
};

/** An enumeration. */
export type SegmentView =
  /** empty */
  | 'A_0'
  /** card */
  | 'A_1';

/** Сессия пользователя. */
export type SessionType = Node & {
  __typename?: 'SessionType';
  /** Количество действий в сессии пользователя */
  activity: Scalars['Int'];
  /** Браузер пользователя */
  browser: Scalars['String'];
  /** Дата сессии пользователя */
  date?: Maybe<Scalars['DateTime']>;
  /** Устройство пользователя */
  device: Scalars['String'];
  /** Количество запросов в сессии пользователя */
  history: Scalars['Int'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** ip-адрес сессии */
  ip: Scalars['String'];
  /** Операционная система пользователя */
  os: Scalars['String'];
  /** Пользователь */
  user: UserType;
};

/** An enumeration. */
export type SettingKindValue =
  /** text */
  | 'A_0'
  /** file */
  | 'A_1'
  /** json */
  | 'A_2'
  /** bool */
  | 'A_4';

/** Настройка приложения. */
export type SettingType = {
  __typename?: 'SettingType';
  id: Scalars['ID'];
  /** Ключ настройки */
  key: Scalars['String'];
  /** Тип значения настройки */
  kindValue: SettingKindValue;
  /** Может ли поле быть изменено */
  readonly: Scalars['Boolean'];
  /** Значение */
  value: Scalars['String'];
};

/** Тип листа. */
export type SheetType = {
  __typename?: 'SheetType';
  /** Может ли пользователь добавлять дочерние строки для строк */
  canAddChildRowDimension: Scalars['Boolean'];
  /** Может ли пользователь изменять лист */
  canChange: Scalars['Boolean'];
  /** Может ли пользователь изменять высоту дочерней строки */
  canChangeChildRowDimensionHeight: Scalars['Boolean'];
  /** Может ли пользователь изменять значение ячейки */
  canChangeValue: Scalars['Boolean'];
  /** Может ли пользователь удалять дочернюю строку, не имеющую собственных дочерних строк */
  canDeleteChildRowDimension: Scalars['Boolean'];
  /** Колонки */
  columns?: Maybe<Array<ColumnDimensionType>>;
  /** Комментарий */
  comment: Scalars['String'];
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  /** Идентификатор */
  id: Scalars['ID'];
  /** Наименование */
  name: Scalars['String'];
  /** Период */
  period?: Maybe<PeriodType>;
  /** Позиция */
  position: Scalars['Int'];
  /** Строки */
  rows?: Maybe<Array<RowDimensionType>>;
  /** Показывать ли подведомственным */
  showChild: Scalars['Boolean'];
  /** Показвать ли головам */
  showHead: Scalars['Boolean'];
  /** Дата обновления */
  updatedAt: Scalars['DateTime'];
};

/** Тип статусов документов. */
export type StatusType = {
  __typename?: 'StatusType';
  /** Комментарий */
  comment?: Maybe<Scalars['String']>;
  /** Можно ли редактировать документ со статусом */
  edit: Scalars['Boolean'];
  id: Scalars['ID'];
  /** Название статуса */
  name: Scalars['String'];
  /** Является ли статус защищенным от изменения */
  protected: Scalars['Boolean'];
};

/** Подписки на сокеты. */
export type Subscription = {
  __typename?: 'Subscription';
  /** Поток новых уведомлений */
  notifications: NotificationsSubscription;
};

export type SupportSubmitMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Загружаемые файлы */
  files?: InputMaybe<Array<Scalars['Upload']>>;
  /** Текст */
  text: Scalars['String'];
  /** Тема */
  topic: Scalars['String'];
};

/** Отправка письма поддержки */
export type SupportSubmitMutationPayload = {
  __typename?: 'SupportSubmitMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

/** Ячейка документа. */
export type TableCellType = {
  __typename?: 'TableCellType';
  /** Выравнивание */
  align?: Maybe<Scalars['String']>;
  /** Заголовок ячейки */
  header: Scalars['String'];
  /** Тип ячейки */
  type?: Maybe<Scalars['String']>;
  /** Значение ячейки */
  value?: Maybe<Scalars['String']>;
};

/** Строка документа. */
export type TableRowType = {
  __typename?: 'TableRowType';
  /** Строка документа */
  cells: Array<Maybe<TableCellType>>;
  /** Индекс строки */
  index: Scalars['Int'];
};

/** Документ, представлющий собой таблицу. */
export type TableType = {
  __typename?: 'TableType';
  /** Заголовки документа */
  headers: Array<Maybe<Scalars['String']>>;
  /** Строки документа */
  rows: Array<Maybe<TableRowType>>;
};

/** Тег */
export type TagType = Node & {
  __typename?: 'TagType';
  /** Дата создания */
  createdAt: Scalars['DateTime'];
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Название */
  name: Scalars['String'];
  /** Пользователь, создавший тег */
  user?: Maybe<UserType>;
};

export type TagTypeConnection = {
  __typename?: 'TagTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<TagTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `TagType` and its cursor. */
export type TagTypeEdge = {
  __typename?: 'TagTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<TagType>;
};

export type UnloadDocumentMutationInput = {
  /** Дополнительные параметры */
  additional?: InputMaybe<Array<Scalars['String']>>;
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Документ */
  documentId: Scalars['ID'];
};

/** Выгрузка документа. */
export type UnloadDocumentMutationPayload = {
  __typename?: 'UnloadDocumentMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Ссылка на сгенерированный файл */
  src?: Maybe<Scalars['String']>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type UnloadFileValueArchiveMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Идентификатор колонки */
  columnId: Scalars['ID'];
  /** Идентификатор документа */
  documentId: Scalars['ID'];
  /** Название архива */
  name: Scalars['String'];
  /** Идентификатор строки */
  rowId: Scalars['ID'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
};

/** Выгрузка архива значения ячейки типа `Файл`. */
export type UnloadFileValueArchiveMutationPayload = {
  __typename?: 'UnloadFileValueArchiveMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки мутации */
  errors: Array<ErrorFieldType>;
  /** Ссылка на сгенерированный архив */
  src?: Maybe<Scalars['String']>;
  /** Успех мутации */
  success: Scalars['Boolean'];
};

export type UploadUsersMutationInput = {
  clientMutationId?: InputMaybe<Scalars['String']>;
  /** Источник данных, файл xlsx или csv */
  file: Scalars['Upload'];
  /** Для загрузки пользователей */
  groupsId?: InputMaybe<Array<InputMaybe<Scalars['Int']>>>;
};

/** Мутация для загрузки пользователей из файла excel | csv. */
export type UploadUsersMutationPayload = {
  __typename?: 'UploadUsersMutationPayload';
  clientMutationId?: Maybe<Scalars['String']>;
  /** Ошибки валидации */
  errors: Array<Maybe<RowFieldErrorType>>;
  /** Успех мутации */
  success: Scalars['Boolean'];
  /** Валидируемый документ */
  table?: Maybe<TableType>;
  /** Загруженные пользователи */
  users?: Maybe<Array<Maybe<UserType>>>;
};

/** Описание пользовательского типа. */
export type UserType = Node & {
  __typename?: 'UserType';
  /** Пользовательское соглашение */
  agreement?: Maybe<Scalars['DateTime']>;
  /** Аватар */
  avatar?: Maybe<Scalars['String']>;
  /** День рождения */
  birthday?: Maybe<Scalars['Date']>;
  /** Дата добавления */
  createdAt: Scalars['DateTime'];
  divisions?: Maybe<Array<Maybe<DivisionModelType>>>;
  /** email */
  email: Scalars['String'];
  /** Имя */
  firstName: Scalars['String'];
  /** Группы пользователя */
  groups: Array<Maybe<GroupType>>;
  /** The ID of the object. */
  id: Scalars['ID'];
  /** Является ли пользователь активным */
  isActive: Scalars['Boolean'];
  /** Фамилия */
  lastName: Scalars['String'];
  notices?: Maybe<NoticeTypeConnection>;
  notifications?: Maybe<NotificationTypeConnection>;
  /** Привилегии пользователя */
  permissions: Array<Maybe<Scalars['String']>>;
  profileValues?: Maybe<Array<Maybe<ProfileValueType>>>;
  /** Сессия пользователя */
  session?: Maybe<SessionType>;
  /** Отчество */
  sirName?: Maybe<Scalars['String']>;
  /** login */
  username: Scalars['String'];
};

/** Описание пользовательского типа. */
export type UserTypeNoticesArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  last?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  user?: InputMaybe<Scalars['ID']>;
};

/** Описание пользовательского типа. */
export type UserTypeNotificationsArgs = {
  after?: InputMaybe<Scalars['String']>;
  before?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  hide?: InputMaybe<Scalars['Boolean']>;
  last?: InputMaybe<Scalars['Int']>;
  notice?: InputMaybe<Scalars['ID']>;
  offset?: InputMaybe<Scalars['Int']>;
  user?: InputMaybe<Scalars['ID']>;
};

export type UserTypeConnection = {
  __typename?: 'UserTypeConnection';
  /** Contains the nodes in this connection. */
  edges: Array<Maybe<UserTypeEdge>>;
  /** Number of nodes. */
  nodeCount: Scalars['Int'];
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Number of items in the queryset. */
  totalCount: Scalars['Int'];
};

/** A Relay edge containing a `UserType` and its cursor. */
export type UserTypeEdge = {
  __typename?: 'UserTypeEdge';
  /** A cursor for use in pagination */
  cursor: Scalars['String'];
  /** The item at the end of the edge */
  node?: Maybe<UserType>;
};

/** Тип значения. */
export type ValueType = {
  __typename?: 'ValueType';
  /** Идентификатор колонки */
  columnId: Scalars['ID'];
  /** Документ */
  document?: Maybe<DocumentType>;
  /** Текст ошибки */
  error?: Maybe<Scalars['String']>;
  id: Scalars['ID'];
  /** Дополнительное поле */
  payload?: Maybe<Scalars['String']>;
  /** Идентификатор строки */
  rowId: Scalars['ID'];
  /** Идентификатор листа */
  sheetId: Scalars['ID'];
  /** Значение */
  value: Scalars['String'];
  /** Валидно ли поле */
  verified: Scalars['Boolean'];
};

export type FileFieldsFragment = { __typename: 'FileType', id: string, name: string, src: string, ext?: string | null, size?: number | null, deleted: boolean, createdAt: any, updatedAt: any };

export type ProfileFieldsFragment = { __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number };

export type ProfileValueFieldsFragment = { __typename: 'ProfileValueType', id: string, value: string, visibility: boolean, createdAt: any, updatedAt: any };

export type SessionFieldsFragment = { __typename: 'SessionType', id: string, ip: string, browser: string, os: string, device: string, date?: any | null };

export type SettingFieldsFragment = { __typename: 'SettingType', id: string, key: string, value: string, kindValue: SettingKindValue, readonly: boolean };

export type UserFieldsFragment = { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any };

export type AddFileMutationVariables = Exact<{
  userId: Scalars['ID'];
  files: Array<Scalars['Upload']> | Scalars['Upload'];
}>;

export type AddFileMutation = { __typename?: 'Mutation', addFile: { __typename?: 'AddFileMutationPayload', success: boolean, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }>, files: Array<{ __typename: 'FileType', id: string, name: string, src: string, ext?: string | null, size?: number | null, deleted: boolean, createdAt: any, updatedAt: any } | null> } };

export type ChangeFileMutationVariables = Exact<{
  fileId: Scalars['ID'];
  field: Scalars['String'];
  value: Scalars['String'];
}>;

export type ChangeFileMutation = { __typename?: 'Mutation', changeFile: { __typename: 'ChangeFileMutationPayload', success: boolean, file?: { __typename: 'FileType', id: string, name: string, src: string, ext?: string | null, size?: number | null, deleted: boolean, createdAt: any, updatedAt: any } | null } };

export type DeleteFileMutationVariables = Exact<{
  fileId: Scalars['ID'];
}>;

export type DeleteFileMutation = { __typename?: 'Mutation', deleteFile: { __typename: 'DeleteFileMutationPayload', success: boolean, id: string } };

export type AddGroupMutationVariables = Exact<{
  name: Scalars['String'];
  permissionFrom?: InputMaybe<Scalars['Int']>;
}>;

export type AddGroupMutation = { __typename?: 'Mutation', addGroup: { __typename: 'AddGroupMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, group?: { __typename: 'GroupType', id: string, name: string, permissions: Array<{ __typename: 'PermissionType', id: string, name: string, codename: string }> } | null } };

export type ChangeGroupNameMutationVariables = Exact<{
  name: Scalars['String'];
  groupId: Scalars['Int'];
}>;

export type ChangeGroupNameMutation = { __typename?: 'Mutation', changeGroupName: { __typename: 'ChangeGroupNameMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, group?: { __typename: 'GroupType', id: string, name: string, permissions: Array<{ __typename: 'PermissionType', id: string, name: string, codename: string }> } | null } };

export type ChangeGroupPermissionsMutationVariables = Exact<{
  groupId: Scalars['Int'];
  permissionsId: Array<InputMaybe<Scalars['Int']>> | InputMaybe<Scalars['Int']>;
  action: ActionRelationShip;
}>;

export type ChangeGroupPermissionsMutation = { __typename?: 'Mutation', changeGroupPermissions: { __typename: 'ChangeGroupPermissionsMutationPayload', success: boolean, permissionsId: Array<number | null>, action: ActionRelationShip, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type DeleteGroupMutationVariables = Exact<{
  groupId: Scalars['Int'];
}>;

export type DeleteGroupMutation = { __typename?: 'Mutation', deleteGroup: { __typename: 'DeleteGroupMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeProfileValueMutationVariables = Exact<{
  profileId: Scalars['ID'];
  userId: Scalars['ID'];
  value: Scalars['String'];
}>;

export type ChangeProfileValueMutation = { __typename?: 'Mutation', changeProfileValue: { __typename: 'ChangeProfileValueMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, profileValue?: { __typename: 'ProfileValueType', id: string, value: string, visibility: boolean, createdAt: any, updatedAt: any, profile: { __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number } } | null } };

export type ChangeProfileVisibilityMutationVariables = Exact<{
  profileValueId: Scalars['ID'];
  visibility: Scalars['Boolean'];
}>;

export type ChangeProfileVisibilityMutation = { __typename?: 'Mutation', changeProfileVisibility: { __typename: 'ChangeProfileVisibilityMutationPayload', success: boolean, profileValue?: { __typename: 'ProfileValueType', id: string, value: string, visibility: boolean, createdAt: any, updatedAt: any, profile: { __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number } } | null, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeSettingsMutationVariables = Exact<{
  userId: Scalars['ID'];
  key: Scalars['String'];
  value: Scalars['String'];
}>;

export type ChangeSettingsMutation = { __typename?: 'Mutation', changeSettings: { __typename: 'ChangeSettingsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, setting?: { __typename: 'SettingType', id: string, key: string, value: string, kindValue: SettingKindValue, readonly: boolean } | null } };

export type ResetSettingsMutationVariables = Exact<{
  userId: Scalars['ID'];
}>;

export type ResetSettingsMutation = { __typename?: 'Mutation', resetSettings: { __typename: 'ResetSettingsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, settings?: Array<{ __typename: 'SettingType', id: string, key: string, value: string, kindValue: SettingKindValue, readonly: boolean }> | null } };

export type SupportSubmitMutationVariables = Exact<{
  topic: Scalars['String'];
  text: Scalars['String'];
  files?: InputMaybe<Array<Scalars['Upload']> | Scalars['Upload']>;
}>;

export type SupportSubmitMutation = { __typename?: 'Mutation', supportSubmit: { __typename?: 'SupportSubmitMutationPayload', success: boolean, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeAvatarMutationVariables = Exact<{
  userId: Scalars['ID'];
  file: Scalars['Upload'];
}>;

export type ChangeAvatarMutation = { __typename?: 'Mutation', changeAvatar: { __typename?: 'ChangeAvatarMutationPayload', success: boolean, avatar: string, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangePasswordMutationVariables = Exact<{
  password: Scalars['String'];
  passwordNew: Scalars['String'];
}>;

export type ChangePasswordMutation = { __typename?: 'Mutation', changePassword: { __typename?: 'ChangePasswordMutationPayload', success: boolean, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeUserGroupsMutationVariables = Exact<{
  userId: Scalars['ID'];
  groupsId: Array<InputMaybe<Scalars['Int']>> | InputMaybe<Scalars['Int']>;
}>;

export type ChangeUserGroupsMutation = { __typename?: 'Mutation', changeUserGroups: { __typename: 'ChangeUserGroupsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, groups?: Array<{ __typename: 'GroupType', id: string, name: string } | null> | null } };

export type ChangeUserPropsMutationVariables = Exact<{
  userId: Scalars['ID'];
  email: Scalars['String'];
  firstName: Scalars['String'];
  lastName: Scalars['String'];
  sirName: Scalars['String'];
  birthday: Scalars['Date'];
}>;

export type ChangeUserPropsMutation = { __typename?: 'Mutation', changeUserProps: { __typename: 'ChangeUserPropsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } } };

export type ConfirmEmailMutationVariables = Exact<{
  email: Scalars['String'];
  code: Scalars['String'];
}>;

export type ConfirmEmailMutation = { __typename?: 'Mutation', confirmEmail: { __typename: 'ConfirmEmailMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, user?: { __typename: 'UserType', email: string, agreement?: any | null } | null } };

export type DeleteSessionsMutationVariables = Exact<{ [key: string]: never; }>;

export type DeleteSessionsMutation = { __typename?: 'Mutation', deleteSessions: { __typename?: 'DeleteSessionsMutationPayload', success: boolean, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type GetTokenMutationVariables = Exact<{
  clientId: Scalars['String'];
  clientSecret: Scalars['String'];
  grantType: Scalars['String'];
  username: Scalars['String'];
  password: Scalars['String'];
}>;

export type GetTokenMutation = { __typename?: 'Mutation', getToken: { __typename?: 'GetTokenMutationPayload', success: boolean, accessToken?: string | null, expiresIn?: number | null, tokenType?: string | null, scope?: string | null, refreshToken?: string | null, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }>, user?: { __typename: 'UserType', birthday?: any | null, isActive: boolean, agreement?: any | null, permissions: Array<string | null>, id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, createdAt: any, session?: { __typename: 'SessionType', id: string, ip: string, browser: string, os: string, device: string, date?: any | null } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null } | null } };

export type LogoutMutationVariables = Exact<{
  sessionId: Scalars['ID'];
}>;

export type LogoutMutation = { __typename?: 'Mutation', logout: { __typename: 'LogoutMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type RecoveryPasswordMutationVariables = Exact<{
  email: Scalars['String'];
}>;

export type RecoveryPasswordMutation = { __typename?: 'Mutation', recoveryPassword: { __typename: 'RecoveryPasswordMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type RegistrationMutationVariables = Exact<{
  username: Scalars['String'];
  email: Scalars['String'];
  lastName: Scalars['String'];
  firstName: Scalars['String'];
  sirName?: InputMaybe<Scalars['String']>;
  birthday: Scalars['Date'];
  password: Scalars['String'];
  agreement: Scalars['Boolean'];
}>;

export type RegistrationMutation = { __typename?: 'Mutation', register: { __typename: 'RegisterMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type RequestCodeMutationVariables = Exact<{
  email: Scalars['String'];
}>;

export type RequestCodeMutation = { __typename?: 'Mutation', requestCode: { __typename: 'RequestCodeMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type RestorePasswordMutationVariables = Exact<{
  token: Scalars['String'];
  password: Scalars['String'];
}>;

export type RestorePasswordMutation = { __typename?: 'Mutation', restorePassword: { __typename: 'RestorePasswordMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type UploadUserMutationVariables = Exact<{
  groupsId?: InputMaybe<Array<InputMaybe<Scalars['Int']>> | InputMaybe<Scalars['Int']>>;
  file: Scalars['Upload'];
}>;

export type UploadUserMutation = { __typename?: 'Mutation', uploadUsers: { __typename?: 'UploadUsersMutationPayload', success: boolean, errors: Array<{ __typename: 'RowFieldErrorType', row: number, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> } | null> } | null>, table?: { __typename?: 'TableType', headers: Array<string | null>, rows: Array<{ __typename?: 'TableRowType', index: number, cells: Array<{ __typename?: 'TableCellType', header: string, value?: string | null } | null> } | null> } | null, users?: Array<{ __typename: 'UserType', id: string, avatar?: string | null, username: string, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any, groups: Array<{ __typename: 'GroupType', id: string, name: string } | null> } | null> | null } };

export type FilesQueryVariables = Exact<{
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
  userId: Scalars['ID'];
  nameContains?: InputMaybe<Scalars['String']>;
}>;

export type FilesQuery = { __typename?: 'Query', files: { __typename: 'FileTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasNextPage: boolean, hasPreviousPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename: 'FileTypeEdge', node?: { __typename: 'FileType', id: string, name: string, src: string, ext?: string | null, size?: number | null, deleted: boolean, createdAt: any, updatedAt: any } | null } | null> } };

export type GroupsQueryVariables = Exact<{ [key: string]: never; }>;

export type GroupsQuery = { __typename?: 'Query', groups: Array<{ __typename: 'GroupType', id: string, name: string, permissions: Array<{ __typename: 'PermissionType', id: string, name: string, codename: string }> }> };

export type LogEntryQueryVariables = Exact<{
  userId?: InputMaybe<Scalars['ID']>;
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type LogEntryQuery = { __typename?: 'Query', logEntry: { __typename: 'LogEntryTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasPreviousPage: boolean, hasNextPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename?: 'LogEntryTypeEdge', node?: { __typename: 'LogEntryType', id: string, action: LogEntryAction, objectId?: number | null, payload?: string | null, createdAt?: any | null, session?: { __typename: 'SessionType', os: string, browser: string } | null, contentType?: { __typename: 'ContentTypeType', appLabel: string, model: string } | null } | null } | null> } };

export type LogEntryGeneralQueryVariables = Exact<{
  first?: InputMaybe<Scalars['Int']>;
  modelContains?: InputMaybe<Scalars['String']>;
  offset?: InputMaybe<Scalars['Int']>;
}>;

export type LogEntryGeneralQuery = { __typename?: 'Query', logEntry: { __typename: 'LogEntryTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasPreviousPage: boolean, hasNextPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename: 'LogEntryTypeEdge', node?: { __typename: 'LogEntryType', id: string, action: LogEntryAction, objectId?: number | null, payload?: string | null, createdAt?: any | null, session?: { __typename: 'SessionType', os: string, browser: string, user: { __typename?: 'UserType', id: string, username: string, lastName: string, firstName: string, sirName?: string | null, email: string } } | null, contentType?: { __typename: 'ContentTypeType', appLabel: string, model: string } | null } | null } | null> } };

export type LogGeneralRequestsQueryVariables = Exact<{
  pageContains?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type LogGeneralRequestsQuery = { __typename?: 'Query', logRequests: { __typename: 'LogRequestTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasPreviousPage: boolean, hasNextPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename: 'LogRequestTypeEdge', node?: { __typename: 'LogRequestType', id: string, page?: string | null, time: number, createdAt: any, session?: { __typename: 'SessionType', browser: string, device: string, os: string, user: { __typename: 'UserType', id: string, username: string, lastName: string, firstName: string, sirName?: string | null, email: string } } | null } | null } | null> } };

export type LogRequestsQueryVariables = Exact<{
  userId?: InputMaybe<Scalars['ID']>;
  pageContains?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type LogRequestsQuery = { __typename?: 'Query', logRequests: { __typename: 'LogRequestTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasNextPage: boolean, hasPreviousPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename?: 'LogRequestTypeEdge', node?: { __typename: 'LogRequestType', id: string, page?: string | null, time: number, createdAt: any, session?: { __typename: 'SessionType', browser: string, device: string, os: string } | null } | null } | null> } };

export type MeQueryVariables = Exact<{ [key: string]: never; }>;

export type MeQuery = { __typename?: 'Query', me?: { __typename: 'UserType', birthday?: any | null, isActive: boolean, agreement?: any | null, permissions: Array<string | null>, id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, createdAt: any, session?: { __typename: 'SessionType', id: string, ip: string, browser: string, os: string, device: string, date?: any | null } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null } | null };

export type PermissionsQueryVariables = Exact<{ [key: string]: never; }>;

export type PermissionsQuery = { __typename?: 'Query', permissions: Array<{ __typename: 'PermissionType', id: string, name: string, codename: string, contentType: { __typename: 'ContentTypeType', appLabel: string, model: string } }> };

export type ProfileInformationQueryVariables = Exact<{
  userId: Scalars['ID'];
}>;

export type ProfileInformationQuery = { __typename?: 'Query', profileInformation: Array<{ __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number, available: Array<{ __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number, value?: { __typename: 'ProfileValueType', id: string, value: string, visibility: boolean, createdAt: any, updatedAt: any } | null }> }> };

export type ProfilesQueryVariables = Exact<{ [key: string]: never; }>;

export type ProfilesQuery = { __typename?: 'Query', profiles: Array<{ __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number, children: Array<{ __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number }> }> };

export type ProfilesValueQueryVariables = Exact<{
  userId: Scalars['ID'];
}>;

export type ProfilesValueQuery = { __typename?: 'Query', profilesValue: Array<{ __typename: 'ProfileValueType', id: string, value: string, visibility: boolean, createdAt: any, updatedAt: any, profile: { __typename: 'ProfileType', id: string, name: string, code: string, kind: ProfileKind, position: number } }> };

export type SessionsQueryVariables = Exact<{
  userId?: InputMaybe<Scalars['ID']>;
}>;

export type SessionsQuery = { __typename?: 'Query', sessions: Array<{ __typename?: 'SessionType', id: string, ip: string, browser: string, device: string, os: string, date?: any | null, activity: number, history: number }> };

export type SettingsQueryVariables = Exact<{ [key: string]: never; }>;

export type SettingsQuery = { __typename?: 'Query', settings: Array<{ __typename: 'SettingType', id: string, key: string, value: string, kindValue: SettingKindValue, readonly: boolean }> };

export type UsersQueryVariables = Exact<{
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
  search?: InputMaybe<Scalars['String']>;
}>;

export type UsersQuery = { __typename?: 'Query', users: { __typename?: 'UserTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasPreviousPage: boolean, hasNextPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename: 'UserTypeEdge', node?: { __typename: 'UserType', id: string, avatar?: string | null, username: string, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any, groups: Array<{ __typename: 'GroupType', id: string, name: string } | null> } | null } | null> } };

export type ActiveStatisticsQueryVariables = Exact<{ [key: string]: never; }>;

export type ActiveStatisticsQuery = { __typename?: 'Query', activeStatistics: { __typename: 'ActiveStatisticsType', queries: Array<{ __typename: 'DateStatisticsType', date: any, value: number } | null>, times: Array<{ __typename: 'DateStatisticsType', date: any, value: number } | null> } };

export type RequestStatisticsQueryVariables = Exact<{ [key: string]: never; }>;

export type RequestStatisticsQuery = { __typename?: 'Query', requestStatistics: { __typename?: 'RequestStatisticsType', browsers: Array<{ __typename?: 'PointStatisticsType', name: string, value: number } | null>, os: Array<{ __typename?: 'PointStatisticsType', name: string, value: number } | null>, device: Array<{ __typename?: 'PointStatisticsType', name: string, value: number } | null> } };

export type AttributeFieldsFragment = { __typename: 'AttributeType', id: string, name: string, placeholder: string, key: string, kind: AttributeKind, default?: string | null, mutable: boolean };

export type CellFieldsFragment = { __typename: 'CellType', id: string, kind: string, editable: boolean, formula?: string | null, comment?: string | null, mask?: string | null, tooltip?: string | null, columnId?: string | null, rowId?: string | null, horizontalAlign?: string | null, verticalAlign?: string | null, size: number, strong: boolean, italic: boolean, strike: boolean, underline?: string | null, color: string, background: string, borderStyle: any, borderColor: any, position: string, globalPosition: string, relatedGlobalPositions: Array<string>, colspan: number, rowspan: number, value?: string | null, verified: boolean, error?: string | null };

export type ColumnDimensionFieldsFragment = { __typename: 'ColumnDimensionType', id: string, index: number, name: string, width?: number | null, fixed: boolean, hidden: boolean, kind: string, createdAt: any, updatedAt: any };

export type DepartmentFieldFragment = { __typename: 'DepartmentType', id: string, name: string, code?: number | null, createdAt: any };

export type DivisionModelFieldsFragment = { __typename: 'DivisionModelType', id: string, model: string, name: string };

export type DocumentFieldsFragment = { __typename: 'DocumentType', id: string, comment: string, version: number, createdAt: any, updatedAt: any, objectId?: string | null, objectName?: string | null };

export type OrganizationFieldFragment = { __typename: 'OrganizationType', id: string, name: string, createdAt: any };

export type PeriodFieldsFragment = { __typename: 'PeriodType', id: string, name: string, status: string, multiple: boolean, privately: boolean, versioning: boolean, start?: any | null, expiration?: any | null, createdAt: any, canAddDocument: boolean, canChangeDivisions: boolean, canChangeGroups: boolean, canChangeUsers: boolean, canChangeSettings: boolean, canChangeSheet: boolean, canDelete: boolean, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }, project?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null, periodGroups?: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null> | null, sheets: Array<{ __typename: 'BaseSheetType', id: string, name: string, showHead: boolean, showChild: boolean, comment: string, createdAt: any, position: number, updatedAt: any } | null> };

export type PeriodGroupFieldsFragment = { __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null };

export type PrivilegesFieldsFragment = { __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any };

export type ProjectFieldsFragment = { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } };

export type RowDimensionFieldsFragment = { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number, name: string, height?: number | null, fixed: boolean, hidden: boolean, dynamic: boolean, aggregation?: string | null, createdAt: any, updatedAt: any, documentId?: string | null, objectId?: string | null, userId?: string | null, parent?: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number } | null, children: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number }>, cells: Array<{ __typename: 'CellType', id: string, kind: string, editable: boolean, formula?: string | null, comment?: string | null, mask?: string | null, tooltip?: string | null, columnId?: string | null, rowId?: string | null, horizontalAlign?: string | null, verticalAlign?: string | null, size: number, strong: boolean, italic: boolean, strike: boolean, underline?: string | null, color: string, background: string, borderStyle: any, borderColor: any, position: string, globalPosition: string, relatedGlobalPositions: Array<string>, colspan: number, rowspan: number, value?: string | null, verified: boolean, error?: string | null }> };

export type SheetFieldsFragment = { __typename: 'SheetType', id: string, name: string, position: number, comment: string, showHead: boolean, showChild: boolean, createdAt: any, updatedAt: any };

export type StatusFieldsFragment = { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean };

export type ValueFieldsFragment = { __typename: 'ValueType', id: string, value: string, payload?: string | null, verified: boolean, error?: string | null, columnId: string, rowId: string, sheetId: string };

export type AddAttributeMutationVariables = Exact<{
  period: Scalars['ID'];
  name: Scalars['String'];
  placeholder: Scalars['String'];
  key: Scalars['String'];
  kind: Scalars['String'];
  default: Scalars['String'];
  mutable?: InputMaybe<Scalars['Boolean']>;
  parent?: InputMaybe<Scalars['ID']>;
}>;

export type AddAttributeMutation = { __typename?: 'Mutation', addAttribute: { __typename?: 'AddAttributeMutationPayload', errors?: Array<{ __typename: 'ErrorType', field: string, messages: Array<string> } | null> | null, attribute?: { __typename: 'AttributeType', id: string, name: string, placeholder: string, key: string, kind: AttributeKind, default?: string | null, mutable: boolean } | null } };

export type ChangeAttributeMutationVariables = Exact<{
  id: Scalars['ID'];
  name: Scalars['String'];
  placeholder: Scalars['String'];
  key: Scalars['String'];
  kind: Scalars['String'];
  default: Scalars['String'];
  mutable?: InputMaybe<Scalars['Boolean']>;
}>;

export type ChangeAttributeMutation = { __typename?: 'Mutation', changeAttribute: { __typename?: 'ChangeAttributeMutationPayload', errors?: Array<{ __typename: 'ErrorType', field: string, messages: Array<string> } | null> | null, attribute?: { __typename: 'AttributeType', id: string, name: string, placeholder: string, key: string, kind: AttributeKind, default?: string | null, mutable: boolean } | null } };

export type ChangeAttributeValueMutationVariables = Exact<{
  attributeId: Scalars['ID'];
  documentId: Scalars['ID'];
  value?: InputMaybe<Scalars['String']>;
}>;

export type ChangeAttributeValueMutation = { __typename?: 'Mutation', changeAttributeValue: { __typename: 'ChangeAttributeValueMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, attributeValue?: { __typename: 'AttributeValueType', id: string, value: string, createdAt: any, updatedAt: any } | null, values?: Array<{ __typename: 'ValueType', id: string, value: string, payload?: string | null, verified: boolean, error?: string | null, columnId: string, rowId: string, sheetId: string } | null> | null } };

export type DeleteAttributeMutationVariables = Exact<{
  attributeId: Scalars['ID'];
}>;

export type DeleteAttributeMutation = { __typename?: 'Mutation', deleteAttribute: { __typename?: 'DeleteAttributeMutationPayload', success: boolean } };

export type AuthCbiasMutationVariables = Exact<{
  uid: Scalars['String'];
  clientId?: InputMaybe<Scalars['String']>;
  clientSecret: Scalars['String'];
}>;

export type AuthCbiasMutation = { __typename?: 'Mutation', authCbias?: { __typename: 'AuthCbiasMutationOutput', success: boolean, token?: { __typename?: 'AuthTokenInfoType', accessToken?: string | null, expiresIn?: number | null, tokenType?: string | null, scope?: string | null, redirectUris?: string | null } | null, user?: { __typename: 'UserType', birthday?: any | null, isActive: boolean, agreement?: any | null, permissions: Array<string | null>, id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, createdAt: any, session?: { __typename: 'SessionType', id: string, ip: string, browser: string, os: string, device: string, date?: any | null } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null } | null } | null };

export type AddBudgetClassificationMutationVariables = Exact<{
  code: Scalars['String'];
  name: Scalars['String'];
}>;

export type AddBudgetClassificationMutation = { __typename?: 'Mutation', addBudgetClassification: { __typename?: 'AddBudgetClassificationMutationPayload', budgetClassification?: { __typename: 'BudgetClassificationType', id: string, code: string, name: string } | null } };

export type ChangeCellDefaultMutationVariables = Exact<{
  cellId: Scalars['ID'];
  default: Scalars['String'];
}>;

export type ChangeCellDefaultMutation = { __typename?: 'Mutation', changeCellDefault: { __typename: 'ChangeCellDefaultPayload', success: boolean, cellId: string, default: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeCellsOptionMutationVariables = Exact<{
  cellIds: Array<Scalars['ID']> | Scalars['ID'];
  field: Scalars['String'];
  value?: InputMaybe<Scalars['String']>;
}>;

export type ChangeCellsOptionMutation = { __typename?: 'Mutation', changeCellsOption: { __typename: 'ChangeCellsOptionMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, changedOptions?: Array<{ __typename: 'ChangedCellOption', cellId: string, field: string, value?: string | null }> | null } };

export type AddChildRowDimensionMutationVariables = Exact<{
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
  parentId: Scalars['ID'];
  index: Scalars['Int'];
  globalIndex: Scalars['Int'];
  globalIndices: Array<GlobalIndicesInputType> | GlobalIndicesInputType;
}>;

export type AddChildRowDimensionMutation = { __typename?: 'Mutation', addChildRowDimension: { __typename: 'AddChildRowDimensionMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, rowDimension: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number, name: string, height?: number | null, fixed: boolean, hidden: boolean, dynamic: boolean, aggregation?: string | null, createdAt: any, updatedAt: any, documentId?: string | null, objectId?: string | null, userId?: string | null, parent?: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number } | null, children: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number }>, cells: Array<{ __typename: 'CellType', id: string, kind: string, editable: boolean, formula?: string | null, comment?: string | null, mask?: string | null, tooltip?: string | null, columnId?: string | null, rowId?: string | null, horizontalAlign?: string | null, verticalAlign?: string | null, size: number, strong: boolean, italic: boolean, strike: boolean, underline?: string | null, color: string, background: string, borderStyle: any, borderColor: any, position: string, globalPosition: string, relatedGlobalPositions: Array<string>, colspan: number, rowspan: number, value?: string | null, verified: boolean, error?: string | null }> } } };

export type AddDocumentMutationVariables = Exact<{
  comment: Scalars['String'];
  periodId: Scalars['ID'];
  statusId: Scalars['ID'];
  divisionId?: InputMaybe<Scalars['ID']>;
  documentId?: InputMaybe<Scalars['ID']>;
}>;

export type AddDocumentMutation = { __typename?: 'Mutation', addDocument: { __typename?: 'AddDocumentMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, document?: { __typename: 'DocumentType', canChange: boolean, id: string, comment: string, version: number, createdAt: any, updatedAt: any, objectId?: string | null, objectName?: string | null, user?: { __typename: 'UserType', id: string } | null, lastStatus?: { __typename: 'DocumentStatusType', id: string, comment: string, createdAt: any, status: { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean } } | null } | null } };

export type AddDocumentDataMutationVariables = Exact<{
  periodId: Scalars['ID'];
  file: Scalars['Upload'];
  statusId: Scalars['ID'];
  comment: Scalars['String'];
}>;

export type AddDocumentDataMutation = { __typename?: 'Mutation', addDocumentData: { __typename: 'AddDocumentDataMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, documents?: Array<{ __typename: 'DocumentType', canChange: boolean, id: string, comment: string, version: number, createdAt: any, updatedAt: any, objectId?: string | null, objectName?: string | null, user?: { __typename: 'UserType', id: string } | null, lastStatus?: { __typename: 'DocumentStatusType', id: string, comment: string, createdAt: any, status: { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean } } | null } | null> | null } };

export type AddDocumentStatusMutationVariables = Exact<{
  comment: Scalars['String'];
  documentId: Scalars['ID'];
  statusId: Scalars['ID'];
}>;

export type AddDocumentStatusMutation = { __typename?: 'Mutation', addDocumentStatus: { __typename: 'AddDocumentStatusMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, documentStatus?: { __typename: 'DocumentStatusType', id: string, comment: string, createdAt: any, status: { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean }, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } } | null } };

export type ChangeChildRowDimensionHeightMutationVariables = Exact<{
  rowDimensionId: Scalars['ID'];
  height?: InputMaybe<Scalars['Int']>;
}>;

export type ChangeChildRowDimensionHeightMutation = { __typename?: 'Mutation', changeChildRowDimensionHeight: { __typename: 'ChangeChildRowDimensionHeightMutationPayload', success: boolean, rowDimensionId: string, height?: number | null, updatedAt: any, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeDocumentCommentMutationVariables = Exact<{
  documentId: Scalars['ID'];
  comment: Scalars['String'];
}>;

export type ChangeDocumentCommentMutation = { __typename?: 'Mutation', changeDocumentComment: { __typename: 'ChangeDocumentCommentMutationPayload', document?: { __typename: 'DocumentType', id: string, comment: string, version: number, createdAt: any, updatedAt: any, objectId?: string | null, objectName?: string | null } | null } };

export type DeleteChildRowDimensionMutationVariables = Exact<{
  rowDimensionId: Scalars['ID'];
}>;

export type DeleteChildRowDimensionMutation = { __typename?: 'Mutation', deleteChildRowDimension: { __typename: 'DeleteChildRowDimensionMutationPayload', success: boolean, rowDimensionId: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type DeleteDocumentStatusMutationVariables = Exact<{
  documentStatusId: Scalars['ID'];
}>;

export type DeleteDocumentStatusMutation = { __typename?: 'Mutation', deleteDocumentStatus: { __typename: 'DeleteDocumentStatusMutationPayload', id: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type UnloadDocumentMutationVariables = Exact<{
  documentId: Scalars['ID'];
  additional?: InputMaybe<Array<Scalars['String']> | Scalars['String']>;
}>;

export type UnloadDocumentMutation = { __typename?: 'Mutation', unloadDocument: { __typename: 'UnloadDocumentMutationPayload', success: boolean, src?: string | null, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type AddDivisionsMutationVariables = Exact<{
  periodId: Scalars['ID'];
  divisionIds?: InputMaybe<Array<Scalars['ID']> | Scalars['ID']>;
}>;

export type AddDivisionsMutation = { __typename?: 'Mutation', addDivisions: { __typename: 'AddDivisionsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, divisions: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> } };

export type AddDivisionFromPeriodMutationVariables = Exact<{
  periodId: Scalars['ID'];
  periodFromId: Scalars['ID'];
}>;

export type AddDivisionFromPeriodMutation = { __typename?: 'Mutation', addDivisionsFromPeriod: { __typename: 'AddDivisionsFromPeriodMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, divisions: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> } };

export type AddDivisionsFromFileMutationVariables = Exact<{
  periodId: Scalars['ID'];
  file: Scalars['Upload'];
}>;

export type AddDivisionsFromFileMutation = { __typename?: 'Mutation', addDivisionsFromFile: { __typename: 'AddDivisionsFromFileMutationPayload', success: boolean, missingDivisions: Array<number | null>, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, divisions: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> } };

export type AddPeriodMutationVariables = Exact<{
  name: Scalars['String'];
  projectId: Scalars['ID'];
  file: Scalars['Upload'];
  multiple: Scalars['Boolean'];
  readonlyFillColor: Scalars['Boolean'];
  versioning: Scalars['Boolean'];
}>;

export type AddPeriodMutation = { __typename?: 'Mutation', addPeriod: { __typename: 'AddPeriodMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, period?: { __typename: 'PeriodType', id: string, name: string, status: string, multiple: boolean, privately: boolean, versioning: boolean, start?: any | null, expiration?: any | null, createdAt: any, canAddDocument: boolean, canChangeDivisions: boolean, canChangeGroups: boolean, canChangeUsers: boolean, canChangeSettings: boolean, canChangeSheet: boolean, canDelete: boolean, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }, project?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null, periodGroups?: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null> | null, sheets: Array<{ __typename: 'BaseSheetType', id: string, name: string, showHead: boolean, showChild: boolean, comment: string, createdAt: any, position: number, updatedAt: any } | null> } | null } };

export type AddPeriodGroupMutationVariables = Exact<{
  name: Scalars['String'];
  periodId: Scalars['ID'];
}>;

export type AddPeriodGroupMutation = { __typename?: 'Mutation', addPeriodGroup: { __typename?: 'AddPeriodGroupMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', messages: Array<string>, field: string }>, periodGroup?: { __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null } };

export type AddPeriodUserMutationVariables = Exact<{
  userId: Scalars['ID'];
  periodId: Scalars['ID'];
  periodGroupIds: Array<Scalars['ID']> | Scalars['ID'];
  privilegesIds: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type AddPeriodUserMutation = { __typename?: 'Mutation', changeUserPeriodGroups: { __typename?: 'ChangeUserPeriodGroupsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, periodGroups: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null>, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } }, changeUserPeriodPrivileges: { __typename?: 'ChangeUserPeriodPrivilegesMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, privileges: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any } | null> } };

export type ChangePeriodMutationVariables = Exact<{
  id: Scalars['ID'];
  name: Scalars['String'];
  status: Scalars['String'];
  multiple: Scalars['Boolean'];
  privately: Scalars['Boolean'];
  start?: InputMaybe<Scalars['Date']>;
  expiration?: InputMaybe<Scalars['Date']>;
  versioning: Scalars['Boolean'];
}>;

export type ChangePeriodMutation = { __typename?: 'Mutation', changePeriod: { __typename: 'ChangePeriodMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, period?: { __typename: 'PeriodType', id: string, name: string, status: string, multiple: boolean, privately: boolean, versioning: boolean, start?: any | null, expiration?: any | null, createdAt: any, canAddDocument: boolean, canChangeDivisions: boolean, canChangeGroups: boolean, canChangeUsers: boolean, canChangeSettings: boolean, canChangeSheet: boolean, canDelete: boolean, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }, project?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null, periodGroups?: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null> | null, sheets: Array<{ __typename: 'BaseSheetType', id: string, name: string, showHead: boolean, showChild: boolean, comment: string, createdAt: any, position: number, updatedAt: any } | null> } | null } };

export type ChangePeriodGroupPrivilegesMutationVariables = Exact<{
  periodGroupId: Scalars['ID'];
  privilegesIds?: InputMaybe<Array<Scalars['ID']> | Scalars['ID']>;
}>;

export type ChangePeriodGroupPrivilegesMutation = { __typename?: 'Mutation', changePeriodGroupPrivileges: { __typename: 'ChangePeriodGroupPrivilegesMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, privileges: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any } | null> } };

export type ChangeShowSheetMutationVariables = Exact<{
  sheetId: Scalars['ID'];
  field: Scalars['String'];
  value: Scalars['Boolean'];
}>;

export type ChangeShowSheetMutation = { __typename?: 'Mutation', changeShowSheet: { __typename: 'ChangeShowSheetMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, sheet?: { __typename: 'BaseSheetType', id: string, name: string, showHead: boolean, showChild: boolean, comment: string, createdAt: any, position: number, updatedAt: any } | null } };

export type ChangeUserPeriodGroupsMutationVariables = Exact<{
  userId: Scalars['ID'];
  periodGroupIds: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type ChangeUserPeriodGroupsMutation = { __typename?: 'Mutation', changeUserPeriodGroups: { __typename?: 'ChangeUserPeriodGroupsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, periodGroups: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null>, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } } };

export type ChangeUserPeriodPrivilegesMutationVariables = Exact<{
  userId: Scalars['ID'];
  periodId: Scalars['ID'];
  privilegesIds: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type ChangeUserPeriodPrivilegesMutation = { __typename?: 'Mutation', changeUserPeriodPrivileges: { __typename?: 'ChangeUserPeriodPrivilegesMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, privileges: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any } | null> } };

export type CopyPeriodGroupsMutationVariables = Exact<{
  periodId: Scalars['ID'];
  selectedPeriodId: Scalars['ID'];
  periodGroupIds: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type CopyPeriodGroupsMutation = { __typename?: 'Mutation', copyPeriodGroups: { __typename?: 'CopyPeriodGroupsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, periodGroups: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null> } };

export type DeleteDivisionMutationVariables = Exact<{
  periodId: Scalars['ID'];
  divisionId: Scalars['ID'];
}>;

export type DeleteDivisionMutation = { __typename?: 'Mutation', deleteDivision: { __typename: 'DeleteDivisionMutationPayload', success: boolean, deleteId: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type DeletePeriodMutationVariables = Exact<{
  id: Scalars['ID'];
}>;

export type DeletePeriodMutation = { __typename?: 'Mutation', deletePeriod: { __typename: 'DeletePeriodMutationPayload', success: boolean, deleteId: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type DeletePeriodGroupMutationVariables = Exact<{
  id: Scalars['ID'];
}>;

export type DeletePeriodGroupMutation = { __typename?: 'Mutation', deletePeriodGroup: { __typename: 'DeletePeriodGroupMutationPayload', success: boolean, deleteId: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type AddProjectMutationVariables = Exact<{
  name: Scalars['String'];
  short: Scalars['String'];
  description: Scalars['String'];
  visibility?: InputMaybe<Scalars['Boolean']>;
  contentType: Scalars['String'];
}>;

export type AddProjectMutation = { __typename?: 'Mutation', addProject: { __typename: 'AddProjectMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, project?: { __typename: 'ProjectType', canChange: boolean, canDelete: boolean, canAddPeriod: boolean, id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null } };

export type ChangeProjectMutationVariables = Exact<{
  id: Scalars['ID'];
  name: Scalars['String'];
  short: Scalars['String'];
  description: Scalars['String'];
  visibility: Scalars['Boolean'];
  archive: Scalars['Boolean'];
}>;

export type ChangeProjectMutation = { __typename?: 'Mutation', changeProject: { __typename: 'ChangeProjectMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, project?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null } };

export type DeleteProjectMutationVariables = Exact<{
  id: Scalars['ID'];
}>;

export type DeleteProjectMutation = { __typename?: 'Mutation', deleteProject: { __typename: 'DeleteProjectMutationPayload', success: boolean, deleteId: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type AddRowDimensionMutationVariables = Exact<{
  sheetId: Scalars['ID'];
  index: Scalars['Int'];
  globalIndex: Scalars['Int'];
  globalIndices: Array<GlobalIndicesInputType> | GlobalIndicesInputType;
}>;

export type AddRowDimensionMutation = { __typename?: 'Mutation', addRowDimension: { __typename: 'AddRowDimensionMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, rowDimension: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number, name: string, height?: number | null, fixed: boolean, hidden: boolean, dynamic: boolean, aggregation?: string | null, createdAt: any, updatedAt: any, documentId?: string | null, objectId?: string | null, userId?: string | null, parent?: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number } | null, children: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number }>, cells: Array<{ __typename: 'CellType', id: string, kind: string, editable: boolean, formula?: string | null, comment?: string | null, mask?: string | null, tooltip?: string | null, columnId?: string | null, rowId?: string | null, horizontalAlign?: string | null, verticalAlign?: string | null, size: number, strong: boolean, italic: boolean, strike: boolean, underline?: string | null, color: string, background: string, borderStyle: any, borderColor: any, position: string, globalPosition: string, relatedGlobalPositions: Array<string>, colspan: number, rowspan: number, value?: string | null, verified: boolean, error?: string | null }> } } };

export type ChangeColumnDimensionMutationVariables = Exact<{
  columnDimensionId: Scalars['ID'];
  width?: InputMaybe<Scalars['Int']>;
  hidden: Scalars['Boolean'];
  kind: Scalars['String'];
}>;

export type ChangeColumnDimensionMutation = { __typename?: 'Mutation', changeColumnDimension: { __typename: 'ChangeColumnDimensionMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, columnDimension?: { __typename: 'ChangeColumnDimensionType', id: string, width?: number | null, hidden: boolean, kind: string, updatedAt: any } | null } };

export type ChangeColumnDimensionsFixedMutationVariables = Exact<{
  columnDimensionIds: Array<Scalars['ID']> | Scalars['ID'];
  fixed: Scalars['Boolean'];
}>;

export type ChangeColumnDimensionsFixedMutation = { __typename?: 'Mutation', changeColumnDimensionsFixed: { __typename?: 'ChangeColumnDimensionsFixedPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, columnDimensions?: Array<{ __typename: 'ChangeColumnDimensionType', id: string, fixed: boolean, updatedAt: any } | null> | null } };

export type ChangeRowDimensionMutationVariables = Exact<{
  rowDimensionId: Scalars['ID'];
  height?: InputMaybe<Scalars['Int']>;
  hidden: Scalars['Boolean'];
  dynamic: Scalars['Boolean'];
}>;

export type ChangeRowDimensionMutation = { __typename?: 'Mutation', changeRowDimension: { __typename?: 'ChangeRowDimensionMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, rowDimension?: { __typename: 'ChangeRowDimensionType', id: string, height?: number | null, hidden: boolean, dynamic: boolean, updatedAt: any } | null } };

export type ChangeRowDimensionsFixedMutationVariables = Exact<{
  rowDimensionIds: Array<Scalars['ID']> | Scalars['ID'];
  fixed: Scalars['Boolean'];
}>;

export type ChangeRowDimensionsFixedMutation = { __typename?: 'Mutation', changeRowDimensionsFixed: { __typename?: 'ChangeRowDimensionsFixedPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, rowDimensions?: Array<{ __typename: 'ChangeRowDimensionType', id: string, fixed: boolean, updatedAt: any } | null> | null } };

export type DeleteRowDimensionMutationVariables = Exact<{
  rowDimensionId: Scalars['ID'];
}>;

export type DeleteRowDimensionMutation = { __typename?: 'Mutation', deleteRowDimension: { __typename: 'DeleteRowDimensionMutationPayload', success: boolean, rowDimensionId: string, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type RenameSheetMutationVariables = Exact<{
  sheetId: Scalars['ID'];
  name: Scalars['String'];
}>;

export type RenameSheetMutation = { __typename?: 'Mutation', renameSheet: { __typename?: 'RenameSheetMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, sheet?: { __typename: 'SheetType', id: string, name: string } | null, cells?: Array<{ __typename: 'CellType', id: string, formula?: string | null } | null> | null } };

export type ChangeFileValueMutationVariables = Exact<{
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
  cellId: Scalars['ID'];
  value: Scalars['String'];
  remainingFiles: Array<Scalars['ID']> | Scalars['ID'];
  newFiles: Array<Scalars['Upload']> | Scalars['Upload'];
}>;

export type ChangeFileValueMutation = { __typename?: 'Mutation', changeFileValue: { __typename?: 'ChangeFileValueMutationPayload', success: boolean, value: string, updatedAt: any, valueFiles?: Array<{ __typename: 'FileType', id: string, name: string, src: string, ext?: string | null, size?: number | null, deleted: boolean, createdAt: any, updatedAt: any } | null> | null } };

export type ChangeValueMutationVariables = Exact<{
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
  cellId: Scalars['ID'];
  value: Scalars['String'];
}>;

export type ChangeValueMutation = { __typename?: 'Mutation', changeValue: { __typename: 'ChangeValueMutationPayload', success: boolean, updatedAt?: any | null, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, values?: Array<{ __typename: 'ValueType', id: string, value: string, payload?: string | null, verified: boolean, error?: string | null, columnId: string, rowId: string, sheetId: string } | null> | null } };

export type UnloadFileValueArchiveMutationVariables = Exact<{
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
  columnId: Scalars['ID'];
  rowId: Scalars['ID'];
  name: Scalars['String'];
}>;

export type UnloadFileValueArchiveMutation = { __typename?: 'Mutation', unloadFileValueArchive: { __typename: 'UnloadFileValueArchiveMutationPayload', success: boolean, src?: string | null, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ActiveBudgetClassificationsQueryVariables = Exact<{
  code?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type ActiveBudgetClassificationsQuery = { __typename?: 'Query', activeBudgetClassifications?: { __typename: 'BudgetClassificationTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', startCursor?: string | null, endCursor?: string | null, hasPreviousPage: boolean, hasNextPage: boolean }, edges: Array<{ __typename: 'BudgetClassificationTypeEdge', node?: { __typename: 'BudgetClassificationType', id: string, code: string, name: string } | null } | null> } | null };

export type AttributesQueryVariables = Exact<{
  periodId: Scalars['ID'];
}>;

export type AttributesQuery = { __typename?: 'Query', attributes: Array<{ __typename: 'AttributeType', id: string, name: string, placeholder: string, key: string, kind: AttributeKind, default?: string | null, mutable: boolean } | null> };

export type AttributesValuesQueryVariables = Exact<{
  documentId: Scalars['ID'];
}>;

export type AttributesValuesQuery = { __typename?: 'Query', attributesValues: Array<{ __typename: 'AttributeValueType', id: string, value: string, createdAt: any, updatedAt: any } | null> };

export type BudgetClassificationsQueryVariables = Exact<{
  code?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type BudgetClassificationsQuery = { __typename?: 'Query', budgetClassifications?: { __typename: 'BudgetClassificationTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', startCursor?: string | null, endCursor?: string | null, hasPreviousPage: boolean, hasNextPage: boolean }, edges: Array<{ __typename: 'BudgetClassificationTypeEdge', node?: { __typename: 'BudgetClassificationType', id: string, code: string, name: string } | null } | null> } | null };

export type DepartmentsQueryVariables = Exact<{ [key: string]: never; }>;

export type DepartmentsQuery = { __typename?: 'Query', departments?: Array<{ __typename: 'DepartmentType', id: string, name: string, code?: number | null, createdAt: any }> | null };

export type DocumentQueryVariables = Exact<{
  documentId: Scalars['ID'];
}>;

export type DocumentQuery = { __typename?: 'Query', document?: { __typename: 'DocumentType', id: string, comment: string, version: number, createdAt: any, updatedAt: any, objectId?: string | null, objectName?: string | null, user?: { __typename: 'UserType', id: string } | null, period?: { __typename: 'PeriodType', id: string, name: string, multiple: boolean, project?: { __typename: 'ProjectType', id: string, name: string, contentType: { __typename: 'ContentTypeType', id: string, model: string } } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, name: string } | null> | null } | null, sheets: Array<{ __typename: 'BaseSheetType', id: string, name: string } | null>, lastStatus?: { __typename: 'DocumentStatusType', id: string, comment: string, status: { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean } } | null } | null };

export type DocumentSheetQueryVariables = Exact<{
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
}>;

export type DocumentSheetQuery = { __typename?: 'Query', documentSheet: { __typename: 'SheetType', canChange: boolean, canChangeValue: boolean, canAddChildRowDimension: boolean, canChangeChildRowDimensionHeight: boolean, canDeleteChildRowDimension: boolean, id: string, name: string, position: number, comment: string, showHead: boolean, showChild: boolean, createdAt: any, updatedAt: any, columns?: Array<{ __typename: 'ColumnDimensionType', id: string, index: number, name: string, width?: number | null, fixed: boolean, hidden: boolean, kind: string, createdAt: any, updatedAt: any }> | null, rows?: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number, name: string, height?: number | null, fixed: boolean, hidden: boolean, dynamic: boolean, aggregation?: string | null, createdAt: any, updatedAt: any, documentId?: string | null, objectId?: string | null, userId?: string | null, parent?: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number } | null, children: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number }>, cells: Array<{ __typename: 'CellType', id: string, kind: string, editable: boolean, formula?: string | null, comment?: string | null, mask?: string | null, tooltip?: string | null, columnId?: string | null, rowId?: string | null, horizontalAlign?: string | null, verticalAlign?: string | null, size: number, strong: boolean, italic: boolean, strike: boolean, underline?: string | null, color: string, background: string, borderStyle: any, borderColor: any, position: string, globalPosition: string, relatedGlobalPositions: Array<string>, colspan: number, rowspan: number, value?: string | null, verified: boolean, error?: string | null }> }> | null } };

export type DocumentStatusesQueryVariables = Exact<{
  documentId: Scalars['ID'];
}>;

export type DocumentStatusesQuery = { __typename?: 'Query', documentStatuses?: Array<{ __typename: 'DocumentStatusType', id: string, comment: string, createdAt: any, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }, status: { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean } }> | null };

export type DocumentsQueryVariables = Exact<{
  periodId: Scalars['ID'];
  divisionIds: Array<Scalars['ID']> | Scalars['ID'];
  lastStatusIds: Array<Scalars['ID']> | Scalars['ID'];
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type DocumentsQuery = { __typename?: 'Query', documents: { __typename?: 'DocumentTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasNextPage: boolean, hasPreviousPage: boolean, startCursor?: string | null, endCursor?: string | null }, edges: Array<{ __typename?: 'DocumentTypeEdge', node?: { __typename: 'DocumentType', canChange: boolean, id: string, comment: string, version: number, createdAt: any, updatedAt: any, objectId?: string | null, objectName?: string | null, user?: { __typename: 'UserType', id: string } | null, lastStatus?: { __typename: 'DocumentStatusType', id: string, comment: string, createdAt: any, status: { __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean } } | null } | null } | null> } };

export type DocumentsSheetQueryVariables = Exact<{
  sheetId: Scalars['ID'];
  documentIds: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type DocumentsSheetQuery = { __typename?: 'Query', documentsSheet: { __typename: 'SheetType', canChange: boolean, canChangeValue: boolean, canAddChildRowDimension: boolean, canChangeChildRowDimensionHeight: boolean, canDeleteChildRowDimension: boolean, id: string, name: string, position: number, comment: string, showHead: boolean, showChild: boolean, createdAt: any, updatedAt: any, columns?: Array<{ __typename: 'ColumnDimensionType', id: string, index: number, name: string, width?: number | null, fixed: boolean, hidden: boolean, kind: string, createdAt: any, updatedAt: any }> | null, rows?: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number, name: string, height?: number | null, fixed: boolean, hidden: boolean, dynamic: boolean, aggregation?: string | null, createdAt: any, updatedAt: any, documentId?: string | null, objectId?: string | null, userId?: string | null, parent?: { __typename: 'RowDimensionType', id: string, index: number, globalIndex: number } | null, children: Array<{ __typename: 'RowDimensionType', id: string, index: number, globalIndex: number }>, cells: Array<{ __typename: 'CellType', id: string, kind: string, editable: boolean, formula?: string | null, comment?: string | null, mask?: string | null, tooltip?: string | null, columnId?: string | null, rowId?: string | null, horizontalAlign?: string | null, verticalAlign?: string | null, size: number, strong: boolean, italic: boolean, strike: boolean, underline?: string | null, color: string, background: string, borderStyle: any, borderColor: any, position: string, globalPosition: string, relatedGlobalPositions: Array<string>, colspan: number, rowspan: number, value?: string | null, verified: boolean, error?: string | null }> }> | null } };

export type OrganizationsQueryVariables = Exact<{ [key: string]: never; }>;

export type OrganizationsQuery = { __typename?: 'Query', organizations?: { __typename?: 'OrganizationTypeConnection', totalCount: number, edges: Array<{ __typename: 'OrganizationTypeEdge', node?: { __typename: 'OrganizationType', id: string, name: string, createdAt: any } | null } | null>, pageInfo: { __typename: 'PageInfo', startCursor?: string | null, endCursor?: string | null, hasNextPage: boolean, hasPreviousPage: boolean } } | null };

export type PeriodQueryVariables = Exact<{
  periodId: Scalars['ID'];
}>;

export type PeriodQuery = { __typename?: 'Query', period: { __typename: 'PeriodType', id: string, name: string, status: string, multiple: boolean, privately: boolean, versioning: boolean, start?: any | null, expiration?: any | null, createdAt: any, canAddDocument: boolean, canChangeDivisions: boolean, canChangeGroups: boolean, canChangeUsers: boolean, canChangeSettings: boolean, canChangeSheet: boolean, canDelete: boolean, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }, project?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null, periodGroups?: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null> | null, sheets: Array<{ __typename: 'BaseSheetType', id: string, name: string, showHead: boolean, showChild: boolean, comment: string, createdAt: any, position: number, updatedAt: any } | null> } };

export type PeriodPossibleDivisionsQueryVariables = Exact<{
  periodId: Scalars['ID'];
  search?: InputMaybe<Scalars['String']>;
  first?: InputMaybe<Scalars['Int']>;
}>;

export type PeriodPossibleDivisionsQuery = { __typename?: 'Query', periodPossibleDivisions?: { __typename?: 'DivisionModelTypeConnection', edges: Array<{ __typename?: 'DivisionModelTypeEdge', node?: { __typename: 'DivisionModelType', id: string, model: string, name: string } | null } | null> } | null };

export type PeriodUsersQueryVariables = Exact<{
  periodId: Scalars['ID'];
}>;

export type PeriodUsersQuery = { __typename?: 'Query', periodUsers: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> };

export type PeriodsQueryVariables = Exact<{
  projectId: Scalars['ID'];
}>;

export type PeriodsQuery = { __typename?: 'Query', periods: Array<{ __typename: 'PeriodType', id: string, name: string, status: string, multiple: boolean, privately: boolean, versioning: boolean, start?: any | null, expiration?: any | null, createdAt: any, canAddDocument: boolean, canChangeDivisions: boolean, canChangeGroups: boolean, canChangeUsers: boolean, canChangeSettings: boolean, canChangeSheet: boolean, canDelete: boolean, user: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }, project?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null, divisions?: Array<{ __typename: 'DivisionModelType', id: string, model: string, name: string } | null> | null, periodGroups?: Array<{ __typename: 'PeriodGroupType', id: string, name: string, createdAt: any, users?: Array<{ __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any }> | null, privileges?: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> | null } | null> | null, sheets: Array<{ __typename: 'BaseSheetType', id: string, name: string, showHead: boolean, showChild: boolean, comment: string, createdAt: any, position: number, updatedAt: any } | null> }> };

export type PrivilegesQueryVariables = Exact<{ [key: string]: never; }>;

export type PrivilegesQuery = { __typename?: 'Query', privileges: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> };

export type ProjectQueryVariables = Exact<{
  projectId: Scalars['ID'];
}>;

export type ProjectQuery = { __typename?: 'Query', project: { __typename: 'ProjectType', canChange: boolean, canDelete: boolean, canAddPeriod: boolean, id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } };

export type ProjectsQueryVariables = Exact<{
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
}>;

export type ProjectsQuery = { __typename?: 'Query', projects?: { __typename: 'ProjectTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', startCursor?: string | null, endCursor?: string | null, hasPreviousPage: boolean, hasNextPage: boolean }, edges: Array<{ __typename?: 'ProjectTypeEdge', node?: { __typename: 'ProjectType', id: string, name: string, short: string, description: string, visibility: boolean, archive: boolean, createdAt: any, contentType: { __typename?: 'ContentTypeType', id: string, model: string } } | null } | null> } | null };

export type StatusesQueryVariables = Exact<{ [key: string]: never; }>;

export type StatusesQuery = { __typename?: 'Query', statuses?: Array<{ __typename: 'StatusType', id: string, name: string, comment?: string | null, edit: boolean, protected: boolean }> | null };

export type UserPeriodPrivilegesQueryVariables = Exact<{
  userId?: InputMaybe<Scalars['ID']>;
  periodId: Scalars['ID'];
}>;

export type UserPeriodPrivilegesQuery = { __typename?: 'Query', userPeriodPrivileges: Array<{ __typename: 'PrivilegeType', id: string, name: string, key: string, createdAt: any }> };

export type ValueFilesQueryVariables = Exact<{
  documentId: Scalars['ID'];
  sheetId: Scalars['ID'];
  columnId: Scalars['ID'];
  rowId: Scalars['ID'];
}>;

export type ValueFilesQuery = { __typename?: 'Query', valueFiles?: Array<{ __typename: 'FileType', id: string, name: string, src: string, ext?: string | null, size?: number | null, deleted: boolean, createdAt: any, updatedAt: any }> | null };

export type MailingFieldsFragment = { __typename: 'MailingType', id: string, dispatchers: any, address: string, header: string, text: string, attachments?: any | null, createdAt: any };

export type NoticeFieldsFragment = { __typename: 'NoticeType', id: string, kind: NoticeKind, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null };

type NoticeInterfaceFields_NoticeEmptyType_Fragment = { __typename: 'NoticeEmptyType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null };

type NoticeInterfaceFields_NoticeMailingType_Fragment = { __typename: 'NoticeMailingType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null };

type NoticeInterfaceFields_NoticePageType_Fragment = { __typename: 'NoticePageType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null };

export type NoticeInterfaceFieldsFragment = NoticeInterfaceFields_NoticeEmptyType_Fragment | NoticeInterfaceFields_NoticeMailingType_Fragment | NoticeInterfaceFields_NoticePageType_Fragment;

export type NotificationFieldsFragment = { __typename: 'NotificationType', id: string, hide: boolean, read: boolean, createdAt: any };

export type ChangeNotificationMutationVariables = Exact<{
  notificationId: Scalars['ID'];
  field: Scalars['String'];
  value: Scalars['Boolean'];
}>;

export type ChangeNotificationMutation = { __typename?: 'Mutation', changeNotification: { __typename: 'ChangeNotificationMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type ChangeNotificationsMutationVariables = Exact<{
  notificationsId: Array<InputMaybe<Scalars['ID']>> | InputMaybe<Scalars['ID']>;
  field: Scalars['String'];
  value: Scalars['Boolean'];
}>;

export type ChangeNotificationsMutation = { __typename?: 'Mutation', changeNotifications: { __typename: 'ChangeNotificationsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type DeleteNoticeMutationVariables = Exact<{
  noticeId: Scalars['ID'];
}>;

export type DeleteNoticeMutation = { __typename?: 'Mutation', deleteNotice: { __typename: 'DeleteNoticeMutationPayload', success: boolean } };

export type NotificationQueryVariables = Exact<{
  notificationId: Scalars['ID'];
}>;

export type NotificationQuery = { __typename?: 'Query', notification: { __typename: 'NotificationType', id: string, hide: boolean, read: boolean, createdAt: any, notice: { __typename: 'NoticeEmptyType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | { __typename: 'NoticeMailingType', id: string, kind: number, payload: string, objectId: string, createdAt: any, mailing?: { __typename: 'MailingType', id: string, dispatchers: any, address: string, header: string, text: string, attachments?: any | null, createdAt: any } | null, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | { __typename: 'NoticePageType', id: string, kind: number, payload: string, objectId: string, createdAt: any, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, sections: Array<{ __typename: 'SectionFilesType', text: string, id: number, kind: number, position: number, files: Array<{ __typename: 'FileType', id: string, name: string, src: string, size?: number | null, ext?: string | null, createdAt: any } | null>, user: { __typename?: 'UserType', id: string } } | { __typename: 'SectionGalleryType', text: string, id: number, kind: number, position: number, images: Array<{ __typename: 'FileType', id: string, name: string, src: string } | null>, user: { __typename?: 'UserType', id: string } } | { __typename: 'SectionTextType', text: string, id: number, kind: number, position: number, user: { __typename?: 'UserType', id: string } } | { __typename: 'SectionUsersType', id: number, kind: number, position: number, users: Array<{ __typename: 'UserType', id: string, avatar?: string | null, lastName: string, firstName: string, sirName?: string | null } | null>, user: { __typename?: 'UserType', id: string } } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null> } | null, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } } };

export type NotificationsQueryVariables = Exact<{
  userId: Scalars['ID'];
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
  hide?: InputMaybe<Scalars['Boolean']>;
}>;

export type NotificationsQuery = { __typename?: 'Query', notifications: { __typename: 'NotificationTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', startCursor?: string | null, endCursor?: string | null, hasNextPage: boolean, hasPreviousPage: boolean }, edges: Array<{ __typename: 'NotificationTypeEdge', node?: { __typename: 'NotificationType', id: string, hide: boolean, read: boolean, createdAt: any, notice: { __typename: 'NoticeEmptyType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | { __typename: 'NoticeMailingType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | { __typename: 'NoticePageType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } } | null } | null> } };

export type NotificationsSubscriptionSubscriptionVariables = Exact<{ [key: string]: never; }>;

export type NotificationsSubscriptionSubscription = { __typename?: 'Subscription', notifications: { __typename: 'NotificationsSubscription', action: ConsumerActionType, id: string, notification?: { __typename: 'NotificationType', id: string, hide: boolean, read: boolean, createdAt: any, notice: { __typename: 'NoticeEmptyType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | { __typename: 'NoticeMailingType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | { __typename: 'NoticePageType', id: string, kind: number, payload: string, objectId: string, createdAt: any, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } } | null } };

export type CategoryFieldsFragment = { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any };

export type PageFieldsFragment = { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null };

export type PageKindFieldsFragment = { __typename: 'PageKindType', id: string, name: string };

type SectionFields_SectionFilesType_Fragment = { __typename: 'SectionFilesType', text: string, id: number, kind: number, position: number, files: Array<{ __typename: 'FileType', id: string, name: string, src: string, size?: number | null, ext?: string | null, createdAt: any } | null>, user: { __typename?: 'UserType', id: string } };

type SectionFields_SectionGalleryType_Fragment = { __typename: 'SectionGalleryType', text: string, id: number, kind: number, position: number, images: Array<{ __typename: 'FileType', id: string, name: string, src: string } | null>, user: { __typename?: 'UserType', id: string } };

type SectionFields_SectionTextType_Fragment = { __typename: 'SectionTextType', text: string, id: number, kind: number, position: number, user: { __typename?: 'UserType', id: string } };

type SectionFields_SectionUsersType_Fragment = { __typename: 'SectionUsersType', id: number, kind: number, position: number, users: Array<{ __typename: 'UserType', id: string, avatar?: string | null, lastName: string, firstName: string, sirName?: string | null } | null>, user: { __typename?: 'UserType', id: string } };

export type SectionFieldsFragment = SectionFields_SectionFilesType_Fragment | SectionFields_SectionGalleryType_Fragment | SectionFields_SectionTextType_Fragment | SectionFields_SectionUsersType_Fragment;

export type SegmentElementFieldsFragment = { __typename: 'SegmentElementType', id: string, view?: SegmentElementView | null, represent?: SegmentElementRepresent | null, width: number, columns: number, pageSize: number };

export type SegementFieldsFragment = { __typename: 'SegmentType', id: string, name?: string | null, align: SegmentAlign, view?: SegmentView | null, position: number, createdAt: any, updatedAt: any };

export type TagFieldsFragment = { __typename: 'TagType', id: string, name: string, createdAt: any };

export type AddCategoryMutationVariables = Exact<{
  avatar?: InputMaybe<Scalars['Upload']>;
  text: Scalars['String'];
  parentId?: InputMaybe<Scalars['ID']>;
}>;

export type AddCategoryMutation = { __typename?: 'Mutation', addCategory: { __typename: 'AddCategoryMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, category?: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any, parent?: { __typename: 'CategoryType', id: string } | null, children: Array<{ __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null> } | null } };

export type ChangeCategoryMutationVariables = Exact<{
  categoryId: Scalars['ID'];
  text: Scalars['String'];
}>;

export type ChangeCategoryMutation = { __typename?: 'Mutation', changeCategory: { __typename: 'ChangeCategoryMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, category?: { __typename: 'CategoryType', id: string, text: string } | null } };

export type ChangeCategoryAvatarMutationVariables = Exact<{
  categoryId: Scalars['ID'];
  avatar?: InputMaybe<Scalars['Upload']>;
}>;

export type ChangeCategoryAvatarMutation = { __typename?: 'Mutation', changeCategoryAvatar: { __typename: 'ChangeCategoryAvatarMutationPayload', success: boolean, category?: { __typename: 'CategoryType', id: string, avatar?: string | null } | null } };

export type DeleteCategoryMutationVariables = Exact<{
  categoryId: Scalars['ID'];
}>;

export type DeleteCategoryMutation = { __typename?: 'Mutation', deleteCategory: { __typename: 'DeleteCategoryMutationPayload', success: boolean } };

export type AddPageMutationVariables = Exact<{
  avatar?: InputMaybe<Scalars['Upload']>;
  parallax?: InputMaybe<Scalars['Boolean']>;
  title: Scalars['String'];
  signature?: InputMaybe<Scalars['String']>;
  hide?: InputMaybe<Scalars['Boolean']>;
  priority?: InputMaybe<Scalars['Boolean']>;
  kindId?: InputMaybe<Scalars['Int']>;
  categoryId: Scalars['ID'];
  tagNames?: InputMaybe<Array<Scalars['String']> | Scalars['String']>;
  text?: InputMaybe<Scalars['String']>;
}>;

export type AddPageMutation = { __typename?: 'Mutation', addPage: { __typename?: 'AddPageMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string } | null } };

export type ChangePageAvatarMutationVariables = Exact<{
  pageId: Scalars['ID'];
  avatar?: InputMaybe<Scalars['Upload']>;
}>;

export type ChangePageAvatarMutation = { __typename?: 'Mutation', changePageAvatar: { __typename?: 'ChangePageAvatarMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } };

export type ChangePageBooleanPropertyMutationVariables = Exact<{
  pageId: Scalars['ID'];
  field: Scalars['String'];
  value: Scalars['Boolean'];
}>;

export type ChangePageBooleanPropertyMutation = { __typename?: 'Mutation', changePageBooleanProperty: { __typename?: 'ChangePageBooleanPropertyMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } };

export type ChangePageCategoryMutationVariables = Exact<{
  pageId: Scalars['ID'];
  categoryId: Scalars['ID'];
}>;

export type ChangePageCategoryMutation = { __typename?: 'Mutation', changePageCategory: { __typename?: 'ChangePageCategoryMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } };

export type ChangePageKindMutationVariables = Exact<{
  pageId: Scalars['ID'];
  pageKindId?: InputMaybe<Scalars['Int']>;
}>;

export type ChangePageKindMutation = { __typename?: 'Mutation', changePageKind: { __typename?: 'ChangePageKindMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } };

export type ChangePageTagsMutationVariables = Exact<{
  pageId: Scalars['ID'];
  tagNames: Array<Scalars['String']> | Scalars['String'];
}>;

export type ChangePageTagsMutation = { __typename?: 'Mutation', changePageTags: { __typename?: 'ChangePageTagsMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } };

export type ChangePageTitleMutationVariables = Exact<{
  pageId: Scalars['ID'];
  title: Scalars['String'];
}>;

export type ChangePageTitleMutation = { __typename?: 'Mutation', changePageTitle: { __typename?: 'ChangePageTitleMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, page?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } };

export type DeletePageMutationVariables = Exact<{
  pageId: Scalars['ID'];
}>;

export type DeletePageMutation = { __typename?: 'Mutation', deletePage: { __typename?: 'DeletePageMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }> } };

export type AddSectionFilesMutationVariables = Exact<{
  pageId: Scalars['ID'];
  text: Scalars['String'];
  files: Array<Scalars['Upload']> | Scalars['Upload'];
}>;

export type AddSectionFilesMutation = { __typename?: 'Mutation', addSectionFiles: { __typename: 'AddSectionFilesMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, section?: { __typename: 'SectionFilesType', text: string, id: number, kind: number, position: number, files: Array<{ __typename: 'FileType', id: string, name: string, src: string, size?: number | null, ext?: string | null, createdAt: any } | null>, user: { __typename?: 'UserType', id: string } } | null } };

export type AddSectionGalleryMutationVariables = Exact<{
  pageId: Scalars['ID'];
  text: Scalars['String'];
  images: Array<Scalars['Upload']> | Scalars['Upload'];
}>;

export type AddSectionGalleryMutation = { __typename?: 'Mutation', addSectionGallery: { __typename: 'AddSectionGalleryMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, section?: { __typename: 'SectionGalleryType', text: string, id: number, kind: number, position: number, images: Array<{ __typename: 'FileType', id: string, name: string, src: string } | null>, user: { __typename?: 'UserType', id: string } } | null } };

export type AddSectionTextMutationVariables = Exact<{
  pageId: Scalars['ID'];
  text: Scalars['String'];
}>;

export type AddSectionTextMutation = { __typename?: 'Mutation', addSectionText: { __typename: 'AddSectionTextMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, section?: { __typename: 'SectionTextType', text: string, id: number, kind: number, position: number, user: { __typename?: 'UserType', id: string } } | null } };

export type ChangeSectionFilesMutationVariables = Exact<{
  sectionId: Scalars['ID'];
  text: Scalars['String'];
  newFiles?: InputMaybe<Array<Scalars['Upload']> | Scalars['Upload']>;
  oldFiles: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type ChangeSectionFilesMutation = { __typename?: 'Mutation', changeSectionFiles: { __typename: 'ChangeSectionFilesMutationPayload', success: boolean, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }>, section?: { __typename: 'SectionFilesType', text: string, id: number, kind: number, position: number, files: Array<{ __typename: 'FileType', id: string, name: string, src: string, size?: number | null, ext?: string | null, createdAt: any } | null>, user: { __typename?: 'UserType', id: string } } | null } };

export type ChangeSectionGalleryMutationVariables = Exact<{
  sectionId: Scalars['ID'];
  text: Scalars['String'];
  newImages?: InputMaybe<Array<Scalars['Upload']> | Scalars['Upload']>;
  oldImages: Array<Scalars['ID']> | Scalars['ID'];
}>;

export type ChangeSectionGalleryMutation = { __typename?: 'Mutation', changeSectionGallery: { __typename: 'ChangeSectionGalleryMutationPayload', success: boolean, errors: Array<{ __typename?: 'ErrorFieldType', field: string, messages: Array<string> }>, section?: { __typename: 'SectionGalleryType', text: string, id: number, kind: number, position: number, images: Array<{ __typename: 'FileType', id: string, name: string, src: string } | null>, user: { __typename?: 'UserType', id: string } } | null } };

export type ChangeSectionTextMutationVariables = Exact<{
  sectionId: Scalars['ID'];
  text: Scalars['String'];
}>;

export type ChangeSectionTextMutation = { __typename?: 'Mutation', changeSectionText: { __typename: 'ChangeSectionTextMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, section?: { __typename: 'SectionTextType', id: number, text: string } | null } };

export type DeleteSectionMutationVariables = Exact<{
  sectionId: Scalars['ID'];
}>;

export type DeleteSectionMutation = { __typename?: 'Mutation', deleteSection: { __typename?: 'DeleteSectionMutationPayload', success: boolean } };

export type AddTagMutationVariables = Exact<{
  name: Scalars['String'];
}>;

export type AddTagMutation = { __typename?: 'Mutation', addTag: { __typename?: 'AddTagMutationPayload', success: boolean, errors: Array<{ __typename: 'ErrorFieldType', field: string, messages: Array<string> }>, tag?: { __typename: 'TagType', id: string, name: string, createdAt: any } | null } };

export type CategoriesQueryVariables = Exact<{
  search?: InputMaybe<Scalars['String']>;
  isNull?: InputMaybe<Scalars['Boolean']>;
  parent?: InputMaybe<Scalars['ID']>;
}>;

export type CategoriesQuery = { __typename?: 'Query', categories: { __typename: 'CategoryTypeConnection', totalCount: number, edges: Array<{ __typename: 'CategoryTypeEdge', node?: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any, children: Array<{ __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null> } | null } | null> } };

export type CategoryQueryVariables = Exact<{
  categoryId: Scalars['ID'];
}>;

export type CategoryQuery = { __typename?: 'Query', category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any, parent?: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null, children: Array<{ __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null>, nc: Array<{ __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null> } };

export type PageQueryVariables = Exact<{
  pageId: Scalars['ID'];
}>;

export type PageQuery = { __typename?: 'Query', page: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, sections: Array<{ __typename: 'SectionFilesType', text: string, id: number, kind: number, position: number, files: Array<{ __typename: 'FileType', id: string, name: string, src: string, size?: number | null, ext?: string | null, createdAt: any } | null>, user: { __typename?: 'UserType', id: string } } | { __typename: 'SectionGalleryType', text: string, id: number, kind: number, position: number, images: Array<{ __typename: 'FileType', id: string, name: string, src: string } | null>, user: { __typename?: 'UserType', id: string } } | { __typename: 'SectionTextType', text: string, id: number, kind: number, position: number, user: { __typename?: 'UserType', id: string } } | { __typename: 'SectionUsersType', id: number, kind: number, position: number, users: Array<{ __typename: 'UserType', id: string, avatar?: string | null, lastName: string, firstName: string, sirName?: string | null } | null>, user: { __typename?: 'UserType', id: string } } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any, parent?: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null, nc: Array<{ __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any } | null> }, kind?: { __typename: 'PageKindType', id: string, name: string } | null, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null> } };

export type PageKindQueryVariables = Exact<{
  pageKindId: Scalars['ID'];
}>;

export type PageKindQuery = { __typename?: 'Query', pageKind: { __typename: 'PageKindType', id: string, name: string } };

export type PageKindsQueryVariables = Exact<{ [key: string]: never; }>;

export type PageKindsQuery = { __typename?: 'Query', pageKinds: Array<{ __typename: 'PageKindType', id: string, name: string }> };

export type PagesQueryVariables = Exact<{
  first?: InputMaybe<Scalars['Int']>;
  after?: InputMaybe<Scalars['String']>;
  categoryId?: InputMaybe<Scalars['ID']>;
  kindId?: InputMaybe<Scalars['ID']>;
  search?: InputMaybe<Scalars['String']>;
}>;

export type PagesQuery = { __typename?: 'Query', pages: { __typename: 'PageTypeConnection', totalCount: number, pageInfo: { __typename: 'PageInfo', hasNextPage: boolean, hasPreviousPage: boolean, endCursor?: string | null, startCursor?: string | null }, edges: Array<{ __typename: 'PageTypeEdge', node?: { __typename: 'PageType', id: string, avatar?: string | null, parallax: boolean, title: string, views: number, signature?: string | null, hide: boolean, priority: boolean, createdAt: any, updatedAt: any, kind?: { __typename: 'PageKindType', id: string, name: string } | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null>, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null } | null } | null> } };

export type SegmentsQueryVariables = Exact<{ [key: string]: never; }>;

export type SegmentsQuery = { __typename?: 'Query', segments: Array<{ __typename: 'SegmentType', id: string, name?: string | null, align: SegmentAlign, view?: SegmentView | null, position: number, createdAt: any, updatedAt: any, elements: Array<{ __typename: 'SegmentElementType', id: string, view?: SegmentElementView | null, represent?: SegmentElementRepresent | null, width: number, columns: number, pageSize: number, pageKind: { __typename: 'PageKindType', id: string, name: string, pages: Array<{ __typename: 'PageType', id: string, avatar?: string | null, title: string, createdAt: any, updatedAt: any, signature?: string | null, preview?: string | null, category: { __typename: 'CategoryType', id: string, avatar?: string | null, text: string, position: number, createdAt: any, updatedAt: any }, user?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null, tags: Array<{ __typename: 'TagType', id: string, name: string, createdAt: any } | null> } | null> } } | null> }> };

export type TagsQueryVariables = Exact<{
  first?: InputMaybe<Scalars['Int']>;
  offset?: InputMaybe<Scalars['Int']>;
  search?: InputMaybe<Scalars['String']>;
}>;

export type TagsQuery = { __typename?: 'Query', tags: { __typename?: 'TagTypeConnection', totalCount: number, edges: Array<{ __typename?: 'TagTypeEdge', node?: { __typename?: 'TagType', id: string, name: string } | null } | null> } };

export type UserInformationQueryVariables = Exact<{
  userId: Scalars['ID'];
}>;

export type UserInformationQuery = { __typename?: 'Query', userInformation?: { __typename: 'UserType', id: string, username: string, avatar?: string | null, email: string, firstName: string, lastName: string, sirName?: string | null, isActive: boolean, createdAt: any } | null };
