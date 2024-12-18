resource "google_compute_instance" "ubuntu_vm" {
  name         = "ubuntu-vm2"
  machine_type = "e2-medium"
  zone         = "europe-west9-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  tags = ["http-server", "https-server"]
}
