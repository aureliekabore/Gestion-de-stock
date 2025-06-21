#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>

#define MAX_PRODUCT 100
#define MAX_NAME_LENGTH 50
#define FILENAME "stock.txt"

typedef struct {
    int id;
    char name[MAX_NAME_LENGTH];
    float price;
    int quantity;
} Product;


Product stock[MAX_PRODUCT];
int productCount = 0;

// ==================== FONCTIONS UTILITAIRES ====================
void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int isIdUnique(int id) {
    for (int i = 0; i < productCount; i++) {
        if (stock[i].id == id) {
            return 0;
        }
    }
    return 1;
}

//Fonction pour trier les produits par nom
void sortProductsByName(){
	for (int i=0;i<productCount -1;i++ ){
		for(int j=i+1; j <productCount ;j++){
			if (strcmp(stock[i].name,stock[j].name)>0){
				Product temp =stock[i];
				stock[i]=stock[j];
				stock [j]=temp;
			}
		}
	}
}
void safeInputString(char *buffer, int length) {
    if (fgets(buffer, length, stdin) != NULL) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') {
            buffer[len-1] = '\0';
        } else {
            clearInputBuffer();
        }
    }
}

int getValidInteger(const char *prompt) {
    int value;
    while (1) {
        printf("%s", prompt);
        if (scanf("%d", &value) == 1) {
            clearInputBuffer();
            return value;
        }
        printf("Saisie invalide. Veuillez entrer un nombre entier.\n");
        clearInputBuffer();
    }
}

float getValidFloat(const char *prompt) {
    float value;
    while (1) {
        printf("%s", prompt);
        if (scanf("%f", &value) == 1) {
            clearInputBuffer();
            return value;
        }
        printf("Saisie invalide. Veuillez entrer un nombre.\n");
        clearInputBuffer();
    }
}

// ==================== FONCTIONS PRINCIPALES ====================
void addProduct() {
    if (productCount >= MAX_PRODUCT) {
        printf("Stock plein! Impossible d'ajouter plus de produits.\n");
        return;
    }

    Product p;
    
    // Saisie de l'ID avec vérification d'unicité
    while (1) {
        p.id = getValidInteger("Entrez l'ID du produit: ");
        
        if (isIdUnique(p.id)) {
            break;
        }
        printf("Cet ID existe deja. Veuillez en choisir un autre.\n");
    }

    // Saisie du nom
    printf("Entrez le nom du produit: ");
    safeInputString(p.name, MAX_NAME_LENGTH);

    // Saisie du prix
    while (1) {
        p.price = getValidFloat("Entrez le prix du produit: ");
        if (p.price > 0) break;
        printf("Le prix doit etre positif.\n");
    }

    // Saisie de la quantité
    while (1) {
        p.quantity = getValidInteger("Entrez la quantite: ");
        if (p.quantity >= 0) break;
        printf("La quantite ne peut pas etre negative.\n");
    }

    stock[productCount++] = p;
    printf("Produit ajoute avec succes!\n");
}

void displayProducts() {
    sortProductsByName();
    if (productCount == 0) {
        printf("Aucun produit dans le stock.\n");
        return;
    }

    printf("\nListe des produits (%d):\n", productCount);
    printf("ID\tNom\t\tPrix\tQuantite\n");
    printf("--------------------------------\n");
    for (int i = 0; i < productCount; i++) {
        printf("%d\t%-15s\t%.2f\t%d\n", 
               stock[i].id, 
               stock[i].name, 
               stock[i].price, 
               stock[i].quantity);
    }
}

void modifyProduct() {
    if (productCount == 0) {
        printf("Aucun produit a modifier.\n");
        return;
    }

    int id = getValidInteger("Entrez l'ID du produit a modifier: ");

    for (int i = 0; i < productCount; i++) {
        if (stock[i].id == id) {
            printf("\nModification du produit [ID: %d]\n", id);
            
            printf("Nouveau nom (actuel: %s): ", stock[i].name);
            safeInputString(stock[i].name, MAX_NAME_LENGTH);

            while (1) {
                stock[i].price = getValidFloat("Nouveau prix: ");
                if (stock[i].price > 0) break;
                printf("Le prix doit etre positif.\n");
            }

            while (1) {
                stock[i].quantity = getValidInteger("Nouvelle quantite: ");
                if (stock[i].quantity >= 0) break;
                printf("La quantite ne peut pas etre negative.\n");
            }

            printf("Produit modifie avec succes!\n");
            return;
        }
    }
    printf("Produit avec ID %d non trouve.\n", id);
}


void deleteProduct() {
	int choice;
    printf("Modifier avec:\n1. ID ou \n2. Nom\nVotre choix: ");
    scanf("%d", &choice);
    if (productCount == 0) {
        printf("Aucun produit a supprimer.\n");
        return;
    }

    int id = getValidInteger("Entrez l'ID du produit a supprimer: ");

    for (int i = 0; i < productCount; i++) {
        if (stock[i].id == id) {
            for (int j = i; j < productCount - 1; j++) {
                stock[j] = stock[j + 1];
            }
            productCount--;
            printf("Produit supprime avec succes!\n");
            return;
        }
    }
    printf("Produit avec ID %d non trouve.\n", id);
}

void searchProduct() {
    if (productCount == 0) {
        printf("Aucun produit a rechercher.\n");
        return;
    }

    int choice;
    while (1) {
        printf("Rechercher par:\n1. ID\n2. Nom\nVotre choix: ");
        if (scanf("%d", &choice) == 1 && (choice == 1 || choice == 2)) {
            clearInputBuffer();
            break;
        }
        printf("Choix invalide. Veuillez entrer 1 ou 2.\n");
        clearInputBuffer();
    }

    if (choice == 1) {
        int id = getValidInteger("Entrez l'ID a rechercher: ");

        for (int i = 0; i < productCount; i++) {
            if (stock[i].id == id) {
                printf("\nProduit trouve:\n");
                printf("ID\t: %d\nNom\t: %s\nPrix\t: %.2f\nQuantite\t: %d\n",
                       stock[i].id, stock[i].name, stock[i].price, stock[i].quantity);
                return;
            }
        }
        printf("Aucun produit trouve avec cet ID.\n");
    } else {
        char name[MAX_NAME_LENGTH];
        printf("Entrez le nom a rechercher: ");
        safeInputString(name, MAX_NAME_LENGTH);

        int found = 0;
        for (int i = 0; i < productCount; i++) {
            if (strcmp(stock[i].name, name) == 0) {
                if (!found) {
                    printf("\nProduits trouves:\n");
                    printf("ID\tNom\t\tPrix\tQuantite\n");
                    printf("--------------------------------\n");
                    found = 1;
                }
                printf("%d\t%-15s\t%.2f\t%d\n",
                       stock[i].id, stock[i].name, stock[i].price, stock[i].quantity);
            }
        }
        if (!found) {
            printf("Aucun produit trouve avec ce nom.\n");
        }
    }
}

void saveToFile() {
    FILE *file = fopen(FILENAME, "w");
    if (file == NULL) {
        printf("Erreur lors de la sauvegarde.\n");
        return;
    }

    for (int i = 0; i < productCount; i++) {
        fprintf(file, "%d\n%s\n%.2f\n%d\n", 
                stock[i].id, 
                stock[i].name, 
                stock[i].price, 
                stock[i].quantity);
    }

    fclose(file);
    printf("Stock sauvegarde dans %s\n", FILENAME);
}

void loadFromFile() {
    FILE *file = fopen(FILENAME, "r");
    if (file == NULL) {
        printf("Aucun fichier de stock trouve. Un nouveau sera cree.\n");
        return;
    }

    productCount = 0;
    char buffer[100];
    
    while (productCount < MAX_PRODUCT) {
        // Lire ID
        if (fgets(buffer, sizeof(buffer), file) == NULL) break;
        stock[productCount].id = atoi(buffer);
        
        // Lire nom
        if (fgets(stock[productCount].name, MAX_NAME_LENGTH, file) == NULL) break;
        size_t len = strlen(stock[productCount].name);
        if (len > 0 && stock[productCount].name[len-1] == '\n') {
            stock[productCount].name[len-1] = '\0';
        }
        
        // Lire prix
        if (fgets(buffer, sizeof(buffer), file) == NULL) break;
        stock[productCount].price = atof(buffer);
        
        // Lire quantité
        if (fgets(buffer, sizeof(buffer), file) == NULL) break;
        stock[productCount].quantity = atoi(buffer);
        
        productCount++;
    }

    fclose(file);
    printf("Stock charge depuis %s (%d produits)\n", FILENAME, productCount);
}

// ==================== MENU PRINCIPAL ====================
void displayMenu() {
    printf("\n=== SYSTEME DE GESTION DE STOCK ===\n");
    printf("1. Ajouter un produit\n");
    printf("2. Afficher tous les produits\n");
    printf("3. Modifier un produit\n");
    printf("4. Supprimer un produit\n");
    printf("5. Rechercher un produit\n");
    printf("6. Sauvegarder\n");
    printf("0. Quitter\n");
    printf("Votre choix: ");
}

int main() {
    setlocale(LC_ALL, ""); // Pour supporter les accents
    
    loadFromFile();
    int choice;

    do {
        displayMenu();
        if (scanf("%d", &choice) == 1) {
            clearInputBuffer();
            switch (choice) {
                case 1: addProduct(); break;
                case 2: displayProducts(); break;
                case 3: modifyProduct(); break;
                case 4: deleteProduct(); break;
                case 5: searchProduct(); break;
                case 6: saveToFile(); break;
                case 0: saveToFile(); printf("Au revoir!\n"); break;
                default: printf("Choix invalide!\n");
            }
        } else {
            clearInputBuffer();
            printf("Veuillez entrer un nombre.\n");
        }
    } while (choice != 0);

    return 0;
}

