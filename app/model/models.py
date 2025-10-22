from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from enum import Enum

# ---------- ENUMS ----------
class ProductCondition(str, Enum):
    new = "new"
    used = "used"
    refurbished = "refurbished"

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    discontinued = "discontinued"

class StockStatus(str, Enum):
    available = "available"
    sold = "sold"
    reserved = "reserved"
    returned = "returned"
    damaged = "damaged"

class MovementType(str, Enum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"
    RETURN = "return"

class PaymentMethod(str, Enum):
    cash = "cash"
    telebirr = "TeleBirr"
    bank = "bank"
    usd = "USD"

class SourceType(str, Enum):
    formal = "formal"
    grey = "grey"

class RepairStatus(str, Enum):
    received = "received"
    in_progress = "in_progress"
    completed = "completed"
    picked_up = "picked_up"
    overdue = "overdue"

class POStatus(str, Enum):
    planned = "planned"
    ordered = "ordered"
    partially_received = "partially_received"
    received = "received"
    cancelled = "cancelled"

# ---------- CORE TABLES ----------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Brand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str] = None

# ---------- PRODUCTS & STOCK ----------
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    description: Optional[str] = None
    condition: ProductCondition
    status: ProductStatus
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_at: Optional[datetime] = None

    stock_items: List["StockItem"] = Relationship(back_populates="product")

class StockItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    sku: str
    serial_or_imei: str
    warranty_period: Optional[str] = None
    qty_on_hand: int = 1
    location: Optional[str] = None
    status: StockStatus
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id")
    source_type: SourceType
    invoice_no: Optional[str] = None
    purchase_date: Optional[date] = None
    cost_price: Optional[float] = None
    landed_cost: Optional[float] = None
    sale_price: Optional[float] = None
    usd_rate_at_purchase: Optional[float] = None
    margin: Optional[float] = None
    price_last_updated: Optional[datetime] = None
    notes: Optional[str] = None
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    product: Optional[Product] = Relationship(back_populates="stock_items")
    price_history: List["PriceHistory"] = Relationship(back_populates="stock_item")
    movements: List["StockMovement"] = Relationship(back_populates="stock_item")
    sale_items: List["SaleItem"] = Relationship(back_populates="stock_item")

class PriceHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_item_id: int = Field(foreign_key="stockitem.id")
    old_price: float
    new_price: float
    changed_by: Optional[int] = Field(default=None, foreign_key="user.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)

    stock_item: Optional[StockItem] = Relationship(back_populates="price_history")

class StockMovement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_item_id: int = Field(foreign_key="stockitem.id")
    movement_type: MovementType
    quantity: int
    reference: Optional[str] = None
    reason: Optional[str] = None
    performed_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    stock_item: Optional[StockItem] = Relationship(back_populates="movements")

# ---------- SALES ----------
class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_date: datetime = Field(default_factory=datetime.utcnow)
    sold_by: Optional[int] = Field(default=None, foreign_key="user.id")
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    payment_method: PaymentMethod
    total_amount: float
    notes: Optional[str] = None

    items: List["SaleItem"] = Relationship(back_populates="sale")

class SaleItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_id: int = Field(foreign_key="sale.id")
    stock_item_id: int = Field(foreign_key="stockitem.id")
    quantity: int
    unit_price: float
    subtotal: float
    profit: float

    sale: Optional[Sale] = Relationship(back_populates="items")
    stock_item: Optional[StockItem] = Relationship(back_populates="sale_items")

# ---------- CASH & EXPENSES ----------
class CashLedger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    opening_balance: float
    total_sales_cash: float
    total_sales_telebirr: float
    total_sales_bank: float
    total_expenses: float
    closing_balance: float
    usd_rate: float

class ExpenseCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    category_id: int = Field(foreign_key="expensecategory.id")
    amount: float
    payment_method: PaymentMethod
    notes: Optional[str] = None
    entered_by: Optional[int] = Field(default=None, foreign_key="user.id")

# ---------- BALANCES ----------
class CustomerBalance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    total_credit: float
    total_paid: float
    outstanding: float
    last_due_date: Optional[date] = None

class SupplierBalance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier_id: int = Field(foreign_key="supplier.id")
    total_owed: float
    total_paid: float
    outstanding: float
    last_due_date: Optional[date] = None

# ---------- USD HISTORY ----------
class USDExchangeRate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    rate: float

# ---------- REPAIRS ----------
class Repair(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    device_description: str
    deposit_amount: float
    status: RepairStatus
    assigned_technician_id: Optional[int] = Field(default=None, foreign_key="user.id")
    received_date: datetime
    due_date: datetime
    completion_date: Optional[datetime] = None
    notes: Optional[str] = None

class RepairItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repair_id: int = Field(foreign_key="repair.id")
    product_id: int = Field(foreign_key="product.id")
    qty_used: int
    unit_cost: float
    unit_sale_price: Optional[float] = None

# ---------- PURCHASE ORDERS ----------
class PurchaseOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier_id: int = Field(foreign_key="supplier.id")
    branch_id: Optional[int] = None
    status: POStatus
    order_date: date
    expected_arrival: date
    usd_rate_at_order: float
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_at: Optional[datetime] = None

class PurchaseOrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    po_id: int = Field(foreign_key="purchaseorder.id")
    product_id: int = Field(foreign_key="product.id")
    qty_ordered: int
    qty_received: int
    unit_cost: float
    notes: Optional[str] = None
