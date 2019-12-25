package models

import "time"

type Temp struct {
	Value     int
	CreatedAt time.Time `gorm:"not null" json:"created_at" sql:"DEFAULT:CURRENT_TIMESTAMP"`
}

type Gas struct {
	Value     int
	Type      string	`gorm:"type:varchar(3)" json:"type" validate:"required"`
	CreatedAt time.Time `gorm:"not null" json:"created_at" sql:"DEFAULT:CURRENT_TIMESTAMP"`
}

//User structure
type User struct {
	ID        uint      `gorm:"primary_key AUTO_INCREMENT" json:"id,omitempty"`
	CreatedAt time.Time `gorm:"not null" json:"created_at" sql:"DEFAULT:CURRENT_TIMESTAMP"`
	Name      string    `gorm:"type:varchar(50)" json:"name" validate:"required"`
	Email     string    `gorm:"type:varchar(50)" json:"email" validate:"required,email"`
	Password  string    `gorm:"type:varchar(50)" json:"password" validate:"required"`
	Role      string    `gorm:"type:varchar(50)" json:"role" validate:"required"`
}

//TableName return name of database table
func (u *User) TableName() string {
	return "user"
}
