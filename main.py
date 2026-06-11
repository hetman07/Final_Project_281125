from ui import menu
from config import config, mongodbconfig, mongoconfig
from db_mysql import DB
from db_mongo import MongoDB
from genres_menu import genres_menu
from films_menu import films_menu
from rating_menu import rating_menu
from stats_menu import stats_menu
from ui import console

def main() -> None:
    """
    Bootstrap the application: connect to both databases, then run the
    main menu loop until the user selects 'Exit'.
    """
    # database connections
    try:
        db = DB(config)
    except Exception as e:
        console.print(f"[bold red]✗  Cannot connect to MySQL: {e}[/bold red]")
        return

    try:
        mongo_db = MongoDB(mongoconfig, mongodbconfig)
    except Exception as e:
        console.print(f"[bold red]✗  Cannot connect to MongoDB: {e}[/bold red]")
        return
    
    # connection confirmation
    try:
        if db.connection.open:
            console.print("[green]✓  MySQL connection established.[/green]")
    except Exception:
        pass
    
    try:
        mongo_db.client.admin.command("ping")
        console.print("[green]✓  MongoDB connection established.[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠  MongoDB ping failed: {e}[/yellow]")
        
    # main menu loop
    while True:
        menu()
        
        try:
            user_command = int(input("Select menu item: ").strip())
        except ValueError:
            console.print("[yellow]⚠  Please enter a number from 1 to 5.[/yellow]")
            continue
        
        if user_command == 5:
            console.print("[dim]Goodbye![/dim]")
            break
        elif user_command == 1:
            films_menu(db, mongo_db)                       
        elif user_command == 2:
            genres_menu(db, mongo_db)           
        elif user_command == 3:
            rating_menu(db, mongo_db)            
        elif user_command == 4:
            stats_menu(mongo_db) 
        else:
            console.print("[yellow]⚠  Please enter a number from 1 to 5.[/yellow]")
            
if __name__ == "__main__":
    main()
     