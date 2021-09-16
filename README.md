# Software utilizzato:
- Python 3.8
- Django
- Pycharm

# Guida all'installazione:
- Clonare la repository o estrarla dallo zip in un percorso a propria scelta
- Aprire il progetto con Pycharm
- Creare un nuovo venv con interprete Python 3.8 (o usarne uno precedentemente configurato)
- Passare al terminale di Pycharm e installare Django:
- - `<pip install Django>`
- Se si sta usando la Community Edition, si può ignorare l'errore "Cannot load facet Django"
- Installare le seguenti librerie:
- - `<pip install django-bootstrap4>`
- - `<pip install django-crispy-forms>`
- - `<pip install django-extra-views>`
- - `<pip install Pillow>`
- Quindi procedere con la creazione del database con i seguenti comandi:
- - `<python manage.py migrate>`
- Per avviare il server, eseguire il seguente comando dal terminale di Pycharm:
- - `<python manage.py runserver 8000>`

# Guida al popolamento del database:
- Collegarsi al db e lanciare tutte le insert salvate in db_test_population/
