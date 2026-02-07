CREATE TABLE posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  post_id VARCHAR(32) NOT NULL UNIQUE,
  source_post_office VARCHAR(120) NOT NULL,
  destination_post_office VARCHAR(120) NOT NULL,
  sender_phone VARCHAR(20) NOT NULL,
  receiver_phone VARCHAR(20) NOT NULL,
  booking_date DATE NOT NULL,
  current_delivery_status VARCHAR(80) NOT NULL DEFAULT 'Booked'
);

CREATE TABLE weather_snapshots (
  id INT AUTO_INCREMENT PRIMARY KEY,
  post_office VARCHAR(120) NOT NULL,
  captured_at DATETIME NOT NULL,
  rainfall_intensity FLOAT NOT NULL,
  wind_speed FLOAT NOT NULL,
  temperature FLOAT NOT NULL,
  flood_risk_level VARCHAR(20) NOT NULL,
  forecast_window VARCHAR(40) NOT NULL
);

CREATE TABLE delay_predictions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  post_id INT NOT NULL,
  weather_snapshot_id INT NOT NULL,
  predicted_delay BOOLEAN NOT NULL,
  predicted_delay_days INT NOT NULL,
  model_version VARCHAR(50) NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (post_id) REFERENCES posts(id),
  FOREIGN KEY (weather_snapshot_id) REFERENCES weather_snapshots(id)
);

CREATE TABLE admin_approvals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  prediction_id INT NOT NULL,
  approved BOOLEAN NOT NULL,
  approved_by VARCHAR(80) NOT NULL,
  approved_at DATETIME NOT NULL,
  remarks VARCHAR(255) NULL,
  FOREIGN KEY (prediction_id) REFERENCES delay_predictions(id)
);

CREATE TABLE sms_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  post_reference VARCHAR(32) NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  message_body VARCHAR(255) NOT NULL,
  sent_at DATETIME NOT NULL,
  provider_reference VARCHAR(120) NULL
);
