from controllers.app_controller import SortingSearchingApp
import customtkinter as ctk

def main():
    root = ctk.CTk()
    app = SortingSearchingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()