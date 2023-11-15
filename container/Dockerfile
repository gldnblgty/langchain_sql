# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Disable the creation of virtual environments
RUN poetry config virtualenvs.create false

# Copy the project files (Poetry files) into the container
COPY pyproject.toml poetry.lock* ./

# Install dependencies
# By default, Poetry installs all packages including dev dependencies.
# Use `--no-dev` to install only the main dependencies
RUN poetry install --no-dev

# Install Uvicorn directly with pip (Windows machines doesn't support so we aren't adding it to Poetry)
RUN pip install uvicorn

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
