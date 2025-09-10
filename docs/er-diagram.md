# Entity Relationship Diagram

This file contains the Entity Relationship (ER) diagram for the Django Bookstore database schema.

## 📊 Database ER Diagram

### Visual ER Diagram
![Database ER Diagram](mermaid-diagram.png)

### Interactive Mermaid Diagram
```mermaid
erDiagram
    User {
        int id PK
        string username UK
        string email
        string first_name
        string last_name
        datetime created_at
        datetime updated_at
        image profile_picture
        string phone_number
        text address
        text bio
        date date_of_birth
    }

    Author {
        int id PK
        string name
        text bio
        date birth_date
        string nationality
        datetime created_at
    }

    Category {
        int id PK
        string name UK
        text description
        datetime created_at
        datetime updated_at
    }

    Publisher {
        int id PK
        string name UK
        text description
        string website
        datetime created_at
        datetime updated_at
    }

    Language {
        int id PK
        string code UK
        string name UK
    }

    Series {
        int id PK
        string name UK
    }

    Genre {
        int id PK
        string name UK
        text description
    }

    Character {
        int id PK
        string name
    }

    Award {
        int id PK
        string name
        int year
        string category
    }

    Book {
        int id PK
        string title
        string isbn UK
        text description
        string goodreads_id
        int author_id FK
        int category_id FK
        int publisher_id FK
        int language_id FK
        int series_id FK
        int page_count
        string book_format
        string edition
        date publication_date
        date first_publication_date
        decimal price
        decimal average_rating
        int num_ratings
        int liked_percent
        int ratings_5_star
        int ratings_4_star
        int ratings_3_star
        int ratings_2_star
        int ratings_1_star
        int bbe_score
        int bbe_votes
        string series_info
        image cover_image
        string cover_image_url
        text settings
        datetime created_at
        datetime updated_at
    }

    Favorite {
        int id PK
        int user_id FK
        int book_id FK
        datetime created_at
    }

    %% Relationships
    User ||--o{ Favorite : "has many"
    Book ||--o{ Favorite : "favorited by many"
    
    Author ||--o{ Book : "writes"
    Category ||--o{ Book : "categorizes"
    Publisher ||--o{ Book : "publishes"
    Language ||--o{ Book : "written in"
    Series ||--o{ Book : "belongs to"
    
    Book }o--o{ Genre : "has genres"
    Book }o--o{ Character : "features characters"
    Book }o--o{ Award : "has won awards"
```

## 🔗 Relationship Legend

### Relationship Types
- **||--o{** : One-to-Many (One entity can have many related entities)
- **}o--o{** : Many-to-Many (Many entities can relate to many other entities)

### Key Symbols
- **PK** : Primary Key
- **FK** : Foreign Key
- **UK** : Unique Key

## 📋 Entity Summary

| Entity | Purpose | Key Relationships |
|--------|---------|-------------------|
| **User** | User accounts and profiles | One-to-Many with Favorite |
| **Book** | Central book information | Many-to-One with Author, Category, Publisher, Language, Series<br>Many-to-Many with Genre, Character, Award<br>One-to-Many with Favorite |
| **Author** | Author information | One-to-Many with Book |
| **Category** | Book categorization | One-to-Many with Book |
| **Publisher** | Publishing companies | One-to-Many with Book |
| **Language** | Book languages | One-to-Many with Book |
| **Series** | Book series | One-to-Many with Book |
| **Genre** | Book genres | Many-to-Many with Book |
| **Character** | Book characters | Many-to-Many with Book |
| **Award** | Literary awards | Many-to-Many with Book |
| **Favorite** | User book preferences | Many-to-One with User and Book |

## 🎯 Key Design Principles

### Normalization
- **3NF Compliance**: Eliminates redundant data
- **Referential Integrity**: Maintains data consistency
- **Atomic Values**: Each field contains single values

### Scalability
- **Indexed Fields**: Optimized for common queries
- **Efficient Relationships**: Minimizes join complexity
- **Flexible Schema**: Supports future enhancements

### Data Integrity
- **Foreign Key Constraints**: Ensures referential integrity
- **Unique Constraints**: Prevents duplicate data
- **Validation Rules**: Enforces data quality

## 🔍 Query Examples

### Common Queries Based on ER Diagram

#### Find all books by an author
```sql
SELECT b.* FROM Book b 
JOIN Author a ON b.author_id = a.id 
WHERE a.name = 'Author Name';
```

#### Find all genres for a book
```sql
SELECT g.* FROM Genre g
JOIN Book_genres bg ON g.id = bg.genre_id
WHERE bg.book_id = 1;
```

#### Find user's favorite books
```sql
SELECT b.* FROM Book b
JOIN Favorite f ON b.id = f.book_id
WHERE f.user_id = 1;
```

#### Find books in a series
```sql
SELECT b.* FROM Book b
JOIN Series s ON b.series_id = s.id
WHERE s.name = 'Series Name';
```

## 📊 Database Statistics

### Estimated Record Counts
- **Books**: 10,000+ records
- **Authors**: 5,000+ records
- **Categories**: 50+ records
- **Publishers**: 1,000+ records
- **Genres**: 100+ records
- **Users**: 1,000+ records
- **Favorites**: 50,000+ records

### Storage Requirements
- **Books Table**: ~50MB (10,000 records)
- **Authors Table**: ~5MB (5,000 records)
- **Favorites Table**: ~10MB (50,000 records)
- **Total Estimated**: ~100MB base data

## 🛠️ Maintenance Considerations

### Regular Maintenance Tasks
- **Index Optimization**: Monitor and optimize indexes
- **Data Cleanup**: Remove orphaned records
- **Statistics Update**: Keep query statistics current
- **Backup Verification**: Ensure backup integrity

### Performance Monitoring
- **Query Performance**: Monitor slow queries
- **Index Usage**: Track index effectiveness
- **Connection Pooling**: Monitor database connections
- **Storage Growth**: Track database size growth

---

*This ER diagram represents the current database schema for the Django Bookstore application. For detailed model information, see the [Database Schema Documentation](database.md).*
