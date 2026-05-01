# Raspberry Pi Deployment

These commands assume Raspberry Pi OS or another Debian-based OS.

## 1. Prepare the Pi

```bash
sudo apt-get update
sudo apt-get install -y git
```

Install Docker if it is not already installed:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
```

Log out and back in after adding your user to the Docker group.

## 2. Clone the Repo

```bash
cd ~
git clone https://github.com/chakri86/jobpilot-pi.git
cd jobpilot-pi
```

If you already created `~/jobpilot-pi/.env`, keep it and copy the project files around it carefully. Do not paste secrets into chat or commit them.

## 3. Create the Environment File

```bash
cp .env.example .env
nano .env
chmod 600 .env
```

Set at minimum:

```env
BOOTSTRAP_ADMIN_EMAIL=avkc@jobpilot.local
BOOTSTRAP_ADMIN_PASSWORD=your-private-password
SECRET_KEY=replace-with-a-long-random-secret
POSTGRES_PASSWORD=replace-with-a-database-password
DATABASE_URL=postgresql+psycopg://jobpilot:replace-with-a-database-password@db:5432/jobpilot
```

## 4. Start JobPilot Pi

```bash
docker compose up --build -d
```

Open:

```text
http://192.168.0.249:5000
```

## 5. Useful Commands

View logs:

```bash
docker compose logs -f app
```

Restart:

```bash
docker compose restart
```

Stop:

```bash
docker compose down
```

Update after pulling new code:

```bash
git pull
docker compose up --build -d
```

## 6. Local Network Security

- Keep `.env` permissioned with `chmod 600 .env`.
- Use a strong `SECRET_KEY`.
- Keep the app on your trusted LAN.
- Do not port-forward the app to the public internet without HTTPS, firewall rules, and stronger hardening.
