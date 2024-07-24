# Django Invoice System Project

## Overview

This project is a Django application for generating and managing invoices. It includes the ability to add items to an invoice, calculate totals, and generate PDFs. The application is containerized using Docker for easy setup and deployment.

## Features

- Create, update, and delete invoices
- Add items to invoices with automatic total calculation
- Generate PDF versions of invoices
- Atomic transactions to ensure data consistency

## Prerequisites

- Docker
- Docker Compose

## Setup and Run

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/kailashpokhrel/invoice-generate.git
cd <REPOSITORY_NAME>

docker-compose up --build

docker-compose run web python manage.py migrate

## Access the application
http://localhost:8000

http://localhost:8000/admin


