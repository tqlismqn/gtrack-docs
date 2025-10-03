# UX — Drivers (Angular 17 + Material)

## Экраны
1) Drivers List  
   - Материал-таблица с фильтрами: поиск, статус (Active/…),
     индикация документов: expired / expiring(≤30д) / valid.
   - Состояния: loading / empty / error.
2) Driver Card  
   - Основные поля профиля, список документов (chips по статусам).
   - Действия: Добавить/редактировать документ, загрузить скан.

## i18n
- Локали: ru, cs, en (через @angular/localize)

## Адаптив
- Mobile ≥360px: карточки, упрощённая таблица.
