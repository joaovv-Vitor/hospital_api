# 🏥 API Sistema Hospitalar

API RESTful moderna desenvolvida com FastAPI para gestão completa de um sistema hospitalar, incluindo pacientes, médicos, atendentes e agendamento de consultas.

## 📋 Índice

- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Documentação da API](#-documentação-da-api)
- [Autenticação](#-autenticação)
- [Modelos de Dados](#-modelos-de-dados)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Docker](#-docker)
- [Desenvolvimento](#-desenvolvimento)

## ✨ Características

- 🔐 **Autenticação JWT** com controle de acesso baseado em roles (RBAC)
- 👥 **Gestão de Usuários** com três perfis: Administrador, Médico e Atendente
- 🏥 **Gestão de Pacientes** com cadastro completo e histórico
- 👨‍⚕️ **Gestão de Médicos** com especialidades e CRM
- 📅 **Sistema de Agendamentos** com controle de status e filtros
- 📊 **Dashboard** com estatísticas em tempo real
- 🚀 **API Assíncrona** para alta performance
- 📝 **Documentação Automática** com Swagger/OpenAPI
- 🐳 **Docker Ready** com docker-compose

## 🛠 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM assíncrono para Python
- **PostgreSQL** - Banco de dados relacional
- **Pydantic** - Validação de dados e configurações
- **JWT** - Autenticação e autorização
- **Bcrypt** - Hash de senhas
- **Uvicorn** - Servidor ASGI de alta performance
- **Docker** - Containerização

## 📦 Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL 16 ou superior
- Docker e Docker Compose (opcional)
- UV (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd hospital_api
```

### 2. Instale as dependências

```bash
uv sync
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql+asyncpg://postgres:banco123@localhost:5432/hospital_db
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ Importante:** Altere a `SECRET_KEY` para uma chave segura em produção!

### 4. Inicie o banco de dados (Docker)

```bash
docker-compose up -d
```

### 5. Execute a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | URL de conexão com PostgreSQL | - |
| `SECRET_KEY` | Chave secreta para JWT | - |
| `ALGORITHM` | Algoritmo de criptografia JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token (minutos) | `30` |

## 📁 Estrutura do Projeto

```
hospital_api/
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   └── v1/
│   │   │       ├── admin.py          # Rotas administrativas
│   │   │       ├── appointment.py    # Rotas de agendamentos
│   │   │       ├── attendant.py     # Rotas de atendentes
│   │   │       ├── auth.py          # Autenticação
│   │   │       ├── dashboard.py     # Dashboard e estatísticas
│   │   │       ├── doctor.py        # Rotas de médicos
│   │   │       ├── patient.py       # Rotas de pacientes
│   │   │       └── user.py          # Rotas de usuários
│   │   ├── deps.py                  # Dependências (auth, roles)
│   │   └── routes.py                # Router principal
│   ├── core/
│   │   ├── config.py                # Configurações
│   │   └── security.py              # Segurança (JWT, hash)
│   ├── db/
│   │   └── database.py              # Configuração do banco
│   ├── models/                      # Modelos SQLAlchemy
│   ├── schemas/                     # Schemas Pydantic
│   ├── services/                    # Lógica de negócio
│   └── main.py                     # Aplicação FastAPI
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## 📚 Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principais

#### 🔐 Autenticação

##### `POST /api/v1/auth/login`
Autentica um usuário e retorna um token JWT.

**Body (form-data):**
```
username: email@exemplo.com
password: senha123
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

#### 👥 Usuários

##### `POST /api/v1/users`
Cria um novo usuário no sistema.

**Permissões:** Qualquer usuário autenticado

**Body:**
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "name": "João Silva",
  "cpf": "12345678901",
  "role": "admin",
  "address": "Rua Exemplo, 123"
}
```

**Resposta:** `201 Created`
```json
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "name": "João Silva",
  "cpf": "12345678901",
  "role": "admin",
  "is_active": true,
  "address": "Rua Exemplo, 123"
}
```

---

#### 🏥 Pacientes

##### `POST /api/v1/patients`
Cadastra um novo paciente.

**Permissões:** `attendant` ou `admin`

**Body:**
```json
{
  "name": "Maria Santos",
  "cpf": "98765432100",
  "birth_date": "1990-05-15",
  "phone": "(11) 98765-4321",
  "address": "Av. Principal, 456"
}
```

**Resposta:** `201 Created`

##### `GET /api/v1/patients`
Lista todos os pacientes cadastrados.

**Permissões:** Qualquer usuário autenticado

**Resposta:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Maria Santos",
    "cpf": "98765432100",
    "birth_date": "1990-05-15",
    "phone": "(11) 98765-4321",
    "address": "Av. Principal, 456"
  }
]
```

---

#### 👨‍⚕️ Médicos

##### `POST /api/v1/admin/doctors`
Registra um novo médico e cria suas credenciais de acesso.

**Permissões:** `admin` apenas

**Body:**
```json
{
  "user": {
    "email": "dr.silva@hospital.com",
    "password": "senha123",
    "name": "Dr. Carlos Silva",
    "cpf": "11122233344",
    "address": "Rua Médica, 789"
  },
  "crm": "CRM12345",
  "specialty": "Cardiologia",
  "phone": "(11) 91234-5678",
  "office_number": "Sala 101"
}
```

**Resposta:** `201 Created`

---

#### 📋 Atendentes

##### `POST /api/v1/admin/attendants`
Registra um novo atendente e cria suas credenciais de acesso.

**Permissões:** `admin` apenas

**Body:**
```json
{
  "user": {
    "email": "atendente@hospital.com",
    "password": "senha123",
    "name": "Ana Costa",
    "cpf": "55566677788",
    "address": "Rua Atendente, 321"
  },
  "employee_id": "EMP001",
  "phone": "(11) 92345-6789"
}
```

**Resposta:** `201 Created`

---

#### 📅 Agendamentos

##### `POST /api/v1/appointments`
Agenda uma nova consulta.

**Permissões:** `attendant` ou `admin`

**Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-12-20T14:30:00",
  "notes": "Consulta de rotina - Pressão alta"
}
```

**Resposta:** `201 Created`
```json
{
  "id": 1,
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2024-12-20T14:30:00",
  "status": "scheduled",
  "notes": "Consulta de rotina - Pressão alta"
}
```

##### `GET /api/v1/appointments`
Lista consultas agendadas.

**Permissões:** Qualquer usuário autenticado
- **Admin/Atendente:** Vê todas as consultas
- **Médico:** Vê apenas suas próprias consultas

**Query Parameters:**
- `date_filter` (opcional): Filtra por data específica (formato: `YYYY-MM-DD`)

**Exemplo:**
```
GET /api/v1/appointments?date_filter=2024-12-20
```

**Resposta:** `200 OK`

##### `PATCH /api/v1/appointments/{appointment_id}/status`
Atualiza o status de uma consulta.

**Permissões:** `admin`, `attendant` ou `doctor`

**Body:**
```json
{
  "status": "completed"
}
```

**Status possíveis:**
- `scheduled` - Agendada
- `completed` - Concluída
- `canceled` - Cancelada

**Resposta:** `200 OK`

---

#### 📊 Dashboard

##### `GET /api/v1/dashboard/stats`
Retorna estatísticas gerais do sistema.

**Permissões:** `admin` ou `attendant`

**Resposta:** `200 OK`
```json
{
  "total_patients": 150,
  "total_doctors": 25,
  "appointments_today": 12,
  "pending_appointments": 8
}
```

---

#### 🏠 Endpoints Gerais

##### `GET /`
Mensagem de boas-vindas.

**Resposta:**
```json
{
  "mensagem": "Bem-vindo à API do Sistema Hospitalar!"
}
```

##### `GET /health`
Verifica o status da API e conexão com o banco de dados.

**Resposta:**
```json
{
  "status": "online",
  "banco_de_dados": "conectado"
}
```

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Tokens). Para acessar endpoints protegidos:

1. Faça login em `/api/v1/auth/login`
2. Copie o `access_token` da resposta
3. Inclua no header das requisições:

```
Authorization: Bearer <access_token>
```

### Controle de Acesso (RBAC)

A API possui três níveis de acesso:

| Role | Descrição | Permissões |
|------|-----------|------------|
| `admin` | Administrador | Acesso total ao sistema |
| `doctor` | Médico | Visualiza apenas suas consultas, pode atualizar status |
| `attendant` | Atendente | Cadastra pacientes, agenda consultas, visualiza todas as consultas |

**Nota:** Administradores têm acesso a todas as rotas automaticamente.

## 📊 Modelos de Dados

### User (Usuário)
- `id` (int): ID único
- `email` (string): Email único
- `hashed_password` (string): Senha criptografada
- `name` (string): Nome completo
- `cpf` (string): CPF único (11 dígitos)
- `role` (enum): `admin`, `doctor` ou `attendant`
- `is_active` (boolean): Status da conta
- `address` (string, opcional): Endereço

### Patient (Paciente)
- `id` (int): ID único
- `name` (string): Nome completo
- `cpf` (string): CPF único (11 dígitos)
- `birth_date` (date): Data de nascimento
- `phone` (string, opcional): Telefone
- `address` (string, opcional): Endereço

### Doctor (Médico)
- `id` (int): ID único
- `crm` (string): CRM único
- `specialty` (string): Especialidade médica
- `phone` (string, opcional): Telefone
- `office_number` (string, opcional): Número da sala
- `is_active_clinical` (boolean): Disponível para consultas
- `user_id` (int): Referência ao User

### Attendant (Atendente)
- `id` (int): ID único
- `employee_id` (string): Matrícula única
- `phone` (string, opcional): Telefone
- `user_id` (int): Referência ao User

### Appointment (Consulta)
- `id` (int): ID único
- `patient_id` (int): Referência ao Patient
- `doctor_id` (int): Referência ao Doctor
- `appointment_date` (datetime): Data e hora da consulta
- `status` (enum): `scheduled`, `completed` ou `canceled`
- `notes` (string, opcional): Observações

## 💡 Exemplos de Uso

### Exemplo 1: Criar um paciente e agendar consulta

```bash
# 1. Login como atendente
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=atendente@hospital.com&password=senha123"

# 2. Criar paciente (usando o token obtido)
curl -X POST "http://localhost:8000/api/v1/patients" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "cpf": "12345678901",
    "birth_date": "1985-03-20",
    "phone": "(11) 98765-4321"
  }'

# 3. Agendar consulta
curl -X POST "http://localhost:8000/api/v1/appointments" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "appointment_date": "2024-12-25T10:00:00",
    "notes": "Consulta de rotina"
  }'
```

### Exemplo 2: Médico visualiza suas consultas

```bash
# Login como médico
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=dr.silva@hospital.com&password=senha123"

# Listar consultas (apenas as do médico logado)
curl -X GET "http://localhost:8000/api/v1/appointments" \
  -H "Authorization: Bearer <token>"

# Filtrar por data específica
curl -X GET "http://localhost:8000/api/v1/appointments?date_filter=2024-12-25" \
  -H "Authorization: Bearer <token>"
```

### Exemplo 3: Atualizar status da consulta

```bash
# Marcar consulta como concluída
curl -X PATCH "http://localhost:8000/api/v1/appointments/1/status" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## 🐳 Docker

### Iniciar apenas o banco de dados

```bash
docker-compose up -d
```

### Parar o banco de dados

```bash
docker-compose down
```

### Ver logs do banco

```bash
docker-compose logs -f db
```

## 🔧 Desenvolvimento

### Executar em modo desenvolvimento

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Estrutura de Código

- **Models** (`app/models/`): Definem a estrutura das tabelas no banco
- **Schemas** (`app/schemas/`): Validação de entrada/saída da API
- **Services** (`app/services/`): Lógica de negócio
- **Routers** (`app/api/routers/`): Endpoints da API
- **Dependencies** (`app/api/deps.py`): Autenticação e autorização

### Boas Práticas

- ✅ Separação de responsabilidades (Models, Schemas, Services, Routers)
- ✅ Validação de dados com Pydantic
- ✅ Controle de acesso baseado em roles
- ✅ Código assíncrono para melhor performance
- ✅ Documentação automática com Swagger

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

**Desenvolvido com ❤️ usando FastAPI**
