VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

deploy:
	ssh hass "rm -rf config/custom_components/better_wol"
	rsync -r custom_components/better_wol/ hass:config/custom_components/better_wol
restart:
	ssh hass "source /etc/profile.d/homeassistant.sh && ha core restart"
configure:
	python3 -m venv $(VENV_PATH)
	$(VENV) pip install -r requirements.txt
clean:
	rm -rf venv
lint:
	$(VENV) pylint custom_components/
