# Maintainer Notes — OpenAPI

- Храним один YAML на версию: `gtrack-v0.yaml`, далее `gtrack-v1.yaml` и т.д.
- Именование схем: `Driver`, `PaginatedDrivers` и т.п.
- Проверка структуры: используйте любой локальный OpenAPI linter/validator, затем `mkdocs build --strict`.
- Если меняете корневой раздел `servers`, оставляйте локальный `http://localhost:3000` как дефолт.
