import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QStackedWidget, QListWidget, QLineEdit, QComboBox,
    QRadioButton, QHBoxLayout, QMessageBox, QScrollArea, QFormLayout, QListWidgetItem
)
from PyQt5.QtCore import Qt

# Données globales
tuteurs = [
    {
        "nom": "Koné",
        "prenom": "Aïda",
        "niveau": "L3",
        "matieres": ["Mathématiques", "Informatique"],
        "disponibilites": ["Lundi 14h-16h", "Mercredi 10h-12h"]
    },
    {
        "nom": "Diop",
        "prenom": "Moussa",
        "niveau": "M1",
        "matieres": ["Physique", "Chimie"],
        "disponibilites": ["Jeudi 9h-11h"]
    },
    {
        "nom": "Sow",
        "prenom": "Fatima",
        "niveau": "M2",
        "matieres": ["Biologie", "Sciences de la Vie"],
        "disponibilites": ["Mardi 15h-17h", "Vendredi 10h-12h"]
    },
    {
        "nom": "Kouamé",
        "prenom": "Yao",
        "niveau": "L2",
        "matieres": ["Économie", "Statistiques"],
        "disponibilites": ["Lundi 10h-12h"]
    }
]

historique_paires = [
    {
        "date": "2025-04-12",
        "tuteur": "Aïda Koné",
        "apprenant": "Bakary Touré",
        "matiere": "Informatique",
        "statut": "En cours"
    },
    {
        "date": "2025-04-08",
        "tuteur": "Moussa Diop",
        "apprenant": "Adama Sarr",
        "matiere": "Physique",
        "statut": "Terminée"
    }
]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plateforme de Tutorat")
        self.setGeometry(100, 100, 500, 500)

        # Variables d'interface
        self.nom_input = None
        self.prenom_input = None
        self.niveau_combo_reg = None
        self.matieres_list = None
        self.disp_combo = None
        self.matiere_combo = None
        self.niveau_combo = None
        self.sort_combo = None
        self.result_list = None
        self.dispo_label = None
        self.tuteur_selectionne = None
        self.filtered_tuteurs = []

        # Création des différentes pages
        self.stacked_widget = QStackedWidget()
        self.menu_page = self.create_menu_page()
        self.search_page = self.create_search_page()
        self.register_page = self.create_register_page()
        self.history_page = self.create_history_page()
        self.dispo_page = self.create_dispo_page()

        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.search_page)
        self.stacked_widget.addWidget(self.register_page)
        self.stacked_widget.addWidget(self.history_page)
        self.stacked_widget.addWidget(self.dispo_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #0f1a2c;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: white;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
                color: #00c98d;
            }
            QPushButton {
                background-color: #00c98d;
                color: black;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
                min-width: 120px;
                max-width: 200px;
                margin: 5px auto;
            }
            QPushButton:hover {
                background-color: #00a573;
            }
            QComboBox, QLineEdit, QListWidget {
                border: 1px solid #2e3b4e;
                border-radius: 4px;
                padding: 6px;
                background-color: #1a2532;
                color: white;
            }
            QRadioButton {
                spacing: 10px;
                padding: 5px;
                color: white;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #00c98d;
            }
            QRadioButton::indicator:checked {
                background-color: #00c98d;
            }
        """)

    def create_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("🎓 Plateforme de Tutorat")
        title.setObjectName("title")
        layout.addWidget(title)
        btn_search = QPushButton("🔍 Chercher un Professeur")
        btn_register = QPushButton("✍ Enregistrer un Tuteur")
        btn_history = QPushButton("📜 Historique")
        btn_search.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_register.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        for btn in [btn_search, btn_register, btn_history]:
            layout.addWidget(btn, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        return page

    def create_search_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("🔍 Rechercher un Tuteur")
        label.setObjectName("title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.matiere_combo = QComboBox()
        toutes_matieres = sorted(set(m for t in tuteurs for m in t["matieres"]))
        self.matiere_combo.addItems([""] + toutes_matieres)

        self.niveau_combo = QComboBox()
        self.niveau_combo.addItems(["", "L1", "L2", "L3", "M1", "M2"])

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Trier par...", "Prénom", "Nom", "Niveau"])

        layout.addWidget(QLabel("Matière"))
        layout.addWidget(self.matiere_combo)
        layout.addWidget(QLabel("Niveau"))
        layout.addWidget(self.niveau_combo)
        layout.addWidget(QLabel("Trier par"))
        layout.addWidget(self.sort_combo)

        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.dispo_label = QLabel("📅 Disponibilités du tuteur sélectionné : ")
        layout.addWidget(self.dispo_label)

        def search():
            self.result_list.clear()
            matiere = self.matiere_combo.currentText().strip().lower()
            niveau = self.niveau_combo.currentText().strip()
            filtres = [t for t in tuteurs if
                       (not matiere or any(m.lower() == matiere for m in t["matieres"])) and
                       (not niveau or t["niveau"] == niveau)]
            critere = self.sort_combo.currentText()
            if critere == "Prénom":
                filtres.sort(key=lambda t: t["prenom"])
            elif critere == "Nom":
                filtres.sort(key=lambda t: t["nom"])
            elif critere == "Niveau":
                filtres.sort(key=lambda t: t["niveau"])
            self.filtered_tuteurs = filtres
            for t in filtres:
                self.result_list.addItem(f"{t['prenom']} {t['nom']} - {t['niveau']}")

        def on_select():
            selected = self.result_list.currentRow()
            if selected >= 0 and selected < len(self.filtered_tuteurs):
                tuteur = self.filtered_tuteurs[selected]
                dispo_text = ", ".join(tuteur["disponibilites"]) or "Aucune disponibilité"
                self.dispo_label.setText(
                    f"📅 Disponibilités de {tuteur['prenom']} {tuteur['nom']} : {dispo_text}"
                )

        def on_select_goto_dispo():
            selected = self.result_list.currentRow()
            if selected >= 0 and selected < len(self.filtered_tuteurs):
                self.tuteur_selectionne = self.filtered_tuteurs[selected]
                self.stacked_widget.setCurrentIndex(4)
                self.dispo_page.update_ui()

        self.result_list.itemClicked.connect(on_select)
        btn_search = QPushButton("Rechercher")
        btn_search.clicked.connect(search)
        layout.addWidget(btn_search, alignment=Qt.AlignCenter)
        btn_select = QPushButton("Voir Disponibilités")
        btn_select.clicked.connect(on_select_goto_dispo)
        layout.addWidget(btn_select, alignment=Qt.AlignCenter)
        btn_back = QPushButton("Retour")
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        page.setLayout(layout)
        return page

    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("✍ Enregistrer un Tuteur")
        label.setObjectName("title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()

        self.niveau_combo_reg = QComboBox()
        self.niveau_combo_reg.addItems(["L1", "L2", "L3", "M1", "M2"])

        self.matieres_list = QListWidget()
        toutes_matieres = [
            "Mathématiques", "Informatique", "Physique", "Chimie",
            "Biologie", "Sciences de la Vie", "Économie", "Statistiques"
        ]
        for m in toutes_matieres:
            item = QListWidgetItem(m)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.matieres_list.addItem(item)

        self.disp_combo = QComboBox()
        self.disp_combo.setEditable(True)
        btn_add_disp = QPushButton("Ajouter disponibilité")

        def add_disponibilite():
            text = self.disp_combo.currentText().strip()
            if text and self.disp_combo.findText(text) == -1:
                self.disp_combo.addItem(text)
                self.disp_combo.setCurrentText("")
        btn_add_disp.clicked.connect(add_disponibilite)

        form_layout = QFormLayout()
        form_layout.addRow("Nom", self.nom_input)
        form_layout.addRow("Prénom", self.prenom_input)
        form_layout.addRow("Niveau", self.niveau_combo_reg)
        form_layout.addRow("Matières", self.matieres_list)
        form_layout.addRow("Disponibilités", self.disp_combo)
        form_layout.addRow("", btn_add_disp)
        layout.addLayout(form_layout)

        def save_tutor():
            nom = self.nom_input.text().strip()
            prenom = self.prenom_input.text().strip()
            niveau = self.niveau_combo_reg.currentText()
            matieres = []
            for i in range(self.matieres_list.count()):
                item = self.matieres_list.item(i)
                if item.checkState() == Qt.Checked:
                    matieres.append(item.text())
            disponibilites = [self.disp_combo.itemText(i) for i in range(self.disp_combo.count())]

            if not all([nom, prenom, niveau]):
                QMessageBox.warning(None, "Erreur", "Remplissez tous les champs obligatoires.")
                return
            if not matieres:
                QMessageBox.warning(None, "Erreur", "Sélectionnez au moins une matière.")
                return
            if not disponibilites:
                QMessageBox.warning(None, "Erreur", "Ajoutez au moins une disponibilité.")
                return

            tuteurs.append({
                "nom": nom,
                "prenom": prenom,
                "niveau": niveau,
                "matieres": matieres,
                "disponibilites": disponibilites
            })
            QMessageBox.information(None, "Succès", "Tuteur enregistré !")
            # Réinitialise le formulaire
            self.nom_input.clear()
            self.prenom_input.clear()
            self.niveau_combo_reg.setCurrentIndex(0)
            for i in range(self.matieres_list.count()):
                self.matieres_list.item(i).setCheckState(Qt.Unchecked)
            self.disp_combo.clear()
            self.stacked_widget.setCurrentIndex(0)

        btn_save = QPushButton("Enregistrer")
        layout.addWidget(btn_save, alignment=Qt.AlignCenter)
        btn_save.clicked.connect(save_tutor)

        btn_back = QPushButton("Retour")
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        page.setLayout(layout)
        return page

    def create_dispo_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.dispo_label = QLabel("📅 Disponibilités du tuteur")
        self.dispo_label.setObjectName("title")
        self.dispo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.dispo_label)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        self.radio_group_layout = QVBoxLayout()
        scroll_content.setLayout(self.radio_group_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        def update_ui():
            while self.radio_group_layout.count():
                widget = self.radio_group_layout.takeAt(0).widget()
                if widget:
                    widget.deleteLater()
            if self.tuteur_selectionne:
                self.dispo_label.setText(
                    f"📅 Disponibilités de {self.tuteur_selectionne['prenom']} {self.tuteur_selectionne['nom']}"
                )
                for disp in self.tuteur_selectionne["disponibilites"]:
                    rb = QRadioButton(disp)
                    self.radio_group_layout.addWidget(rb)
            else:
                self.dispo_label.setText("❌ Aucun tuteur sélectionné.")

        def confirmer():
            selected = None
            for i in range(self.radio_group_layout.count()):
                widget = self.radio_group_layout.itemAt(i).widget()
                if isinstance(widget, QRadioButton) and widget.isChecked():
                    selected = widget.text()
                    break
            if not selected:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une disponibilité.")
                return
            historique_paires.append({
                "date": "Aujourd’hui",
                "tuteur": f"{self.tuteur_selectionne['prenom']} {self.tuteur_selectionne['nom']}",
                "apprenant": "Nouvel Apprenant",
                "matiere": "Mathématiques",
                "statut": "En cours"
            })
            self.history_page.update_history()
            QMessageBox.information(self, "Succès", "Demande envoyée !")
            self.stacked_widget.setCurrentIndex(1)

        btn_confirmer = QPushButton("Demander ce tutorat")
        layout.addWidget(btn_confirmer, alignment=Qt.AlignCenter)
        btn_confirmer.clicked.connect(confirmer)

        btn_back = QPushButton("Retour")
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        page.setLayout(layout)
        page.update_ui = update_ui
        return page

    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        label = QLabel("📜 Historique des Paires")
        label.setObjectName("title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

        def update_history():
            self.history_list.clear()
            for h in historique_paires:
                self.history_list.addItem(f"{h['date']} | {h['tuteur']} → {h['apprenant']} | {h['matiere']} ({h['statut']})")

        page.update_history = update_history
        update_history()
        btn_back = QPushButton("Retour")
        layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        page.setLayout(layout)
        return page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())