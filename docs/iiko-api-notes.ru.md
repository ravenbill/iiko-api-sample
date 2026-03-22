# Заметки по iiko API

## Базовые сведения о Cloud API

- Официальная точка входа в документацию: `https://api-ru.iiko.services/docs`
- Базовый URL для API-запросов: `https://api-ru.iiko.services`
- Аутентификация начинается с запроса access token
- Запрос `/api/1/access_token` использует поле `apiLogin`
- Ответ на запрос access token включает `correlationId` и `token`

## Что такое `apiLogin`

`apiLogin` — это интеграционный логин для конкретного клиента iiko. Это не обычный пароль конечного пользователя.

В исследованных материалах iiko `apiLogin` описывается так:

> API login. It is set in iikoWeb.

Это означает, что наше приложение должно хранить один `apiLogin` на клиента и использовать его для получения access token перед вызовом остальных методов Cloud API.

## Где получить `apiLogin`

Справочные материалы iiko показывают, что настройки Cloud API управляются через back office / iikoWeb.

Наблюдаемый путь:

`Обмен данными -> Настройка iikoTransport`

После этого iiko открывает страницу настроек Cloud API в iikoWeb.

Практический вывод:

- у клиента должен быть доступ в iikoWeb
- кто-то с достаточными правами должен открыть настройки Cloud API
- значение `apiLogin` для этого клиента настраивается или берется там

Если в аккаунте ресторана эти настройки недоступны, клиенту, вероятно, понадобится помощь администратора iiko, дилера или интегратора.

## Как мы планируем моделировать это локально

Мы храним по одной именованной записи клиента в `.env`.

Пример:

```dotenv
IIKO_CLIENTS=client_one,client_two

IIKO_CLIENT_CLIENT_ONE_NAME=Client One
IIKO_CLIENT_CLIENT_ONE_API_LOGIN=replace-with-client-one-login

IIKO_CLIENT_CLIENT_TWO_NAME=Client Two
IIKO_CLIENT_CLIENT_TWO_API_LOGIN=replace-with-client-two-login
```

Это позволит будущим командам работать так:

- один клиент: `--client client_one`
- несколько клиентов: `--clients client_one,client_two`

## Официальные заметки по customer API

- `Create or update customer` официально документирован как метод, работающий по `id`, `phone` или `card track`
- `Get customer info` официально поддерживает значения `type`: `phone`, `cardTrack`, `cardNumber`, `email`, `id`
- Официальная схема create/update customer включает такие поля, как:
  - `id`
  - `phone`
  - `cardTrack`
  - `cardNumber`
  - `name`
  - `middleName`
  - `surName`
  - `birthday`
  - `email`
  - `sex`
  - `consentStatus`
  - `shouldReceiveLoyaltyInfo`
  - `shouldReceivePromoActionsInfo`
  - `referrerId`
  - `userData`
  - `isDeleted`
  - `organizationId`

## Уточненные открытые вопросы

- требуется подтвердить, нужны ли для каких-то клиентов региональные base URL
- требуется подтвердить, кто на стороне клиента имеет право видеть или получать `apiLogin`
- нужно выбрать первое правило уникальности гостя для нашей команды create-guest: самым простым первым кандидатом выглядит `phone`, но API также поддерживает `id` и `cardTrack`
- нужно подтвердить точный путь для проверки баланса по track number в официальной документации перед началом balance tool

## Ссылки

- `https://api-ru.iiko.services`
- `https://api-ru.iiko.services/docs`
- `https://ru.iiko.help/smart/project-iikoweb/iikocloudapi`
- `https://ru.iiko.help/articles/api-documentations/kak-podklyuchit-vneshniy-api`
- `https://api.iiko.ru/`
