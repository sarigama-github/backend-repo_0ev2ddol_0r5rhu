"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import date

# Example schemas (retain for reference/testing)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# --------------------------------------------------
# CRM Schemas (used by the AI-powered CRM suite)
# --------------------------------------------------

class Company(BaseModel):
    name: str = Field(..., description="Company name")
    domain: Optional[str] = Field(None, description="Company website domain")
    industry: Optional[str] = Field(None, description="Industry vertical")
    size: Optional[str] = Field(None, description="Company size e.g., 1-10, 11-50")
    country: Optional[str] = Field(None, description="Headquarters country")

class Contact(BaseModel):
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    company: Optional[str] = Field(None, description="Associated company name")
    title: Optional[str] = Field(None, description="Job title")
    status: Literal['lead','prospect','customer','churned'] = Field('lead', description="Lifecycle stage")
    owner: Optional[str] = Field(None, description="Account owner or rep")

class Deal(BaseModel):
    name: str = Field(..., description="Deal name")
    amount: float = Field(..., ge=0, description="Deal amount")
    stage: Literal['new','qualified','proposal','won','lost'] = Field('new', description="Sales stage")
    close_date: Optional[date] = Field(None, description="Expected close date")
    company: Optional[str] = Field(None, description="Associated company")
    contact: Optional[str] = Field(None, description="Primary contact")
    owner: Optional[str] = Field(None, description="Deal owner")

class Activity(BaseModel):
    type: Literal['call','email','meeting','note','task'] = Field(..., description="Activity type")
    subject: str = Field(..., description="Short subject")
    notes: Optional[str] = Field(None, description="Detailed notes")
    due_date: Optional[date] = Field(None, description="Due date for tasks/meetings")
    company: Optional[str] = Field(None, description="Related company")
    contact: Optional[str] = Field(None, description="Related contact")
    deal: Optional[str] = Field(None, description="Related deal")
    owner: Optional[str] = Field(None, description="Activity owner")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
