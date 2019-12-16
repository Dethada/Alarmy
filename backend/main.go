package main

import (
        "log"
        "net/http"

        graphql "github.com/graph-gophers/graphql-go"
        "github.com/graph-gophers/graphql-go/relay"

        "github.com/jinzhu/gorm"
        _ "github.com/jinzhu/gorm/dialects/postgres"

	"github.com/joho/godotenv"
)

type query struct{}

func (_ *query) Hello() string { return "Hello, world!" }

func main() {
	e := godotenv.Load() //Load .env file
	if e != nil {
		fmt.Print(e)
	}

	username := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASS")
	dbName := os.Getenv("DB_NAME")
	dbHost := os.Getenv("DB_HOST")


	dbUri := fmt.Sprintf("host=%s user=%s dbname=%s sslmode=disable password=%s", dbHost, username, dbName, password) //Build connection string
	fmt.Println(dbUri)

	db, err := gorm.Open("postgres", dbUri)
	if err != nil {
		fmt.Print(err)
	}
	defer db.Close()

        s := `
               type Query {
                        hello: String!
                }
        `
        schema := graphql.MustParseSchema(s, &query{})
        http.Handle("/query", &relay.Handler{Schema: schema})
        log.Fatal(http.ListenAndServe(":9000", nil))
}
