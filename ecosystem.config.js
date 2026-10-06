module.exports = {
  apps: [
    {
      name: "sugo-bot",
      script: "/home/webuser/apps/sugo-bot/main.py",
      interpreter: "/home/webuser/apps/sugo-bot/venv/bin/python",

      // Manejo limpio de cierres
      kill_timeout: 5000,
      wait_ready: false,
      listen_timeout: 5000,

      // Reinicio automático si se cae
      autorestart: true,
      max_memory_restart: "300M",

      // Reinicio diario a las 3 AM
      cron_restart: "0 3 * * *",

      // Logs ordenados
      out_file: "/home/webuser/.pm2/logs/sugo-bot-out.log",
      error_file: "/home/webuser/.pm2/logs/sugo-bot-error.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss"
    }
  ]
}
