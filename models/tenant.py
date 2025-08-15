from utils.db import connect
from models.house import update_house_status

def add_tenant(name, phone, house_id):
    """Add a new tenant and mark appartement as occupied"""
    conn = connect()
    cur = conn.cursor()
    try:
        # First check if appartement exists and is vacant
        cur.execute("SELECT status FROM houses WHERE id = ?", (house_id,))
        house = cur.fetchone()
        
        if not house:
            raise ValueError("Appartement does not exist")
        if house[0] != 'vacant':
            raise ValueError("Appartement is already occupied")

        # Add tenant
        cur.execute("""
            INSERT INTO tenants (name, phone, house_id)
            VALUES (?, ?, ?)
        """, (name, phone, house_id))
        
        # Mark appartement as occupied
        update_house_status(house_id, 'occupied')
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding tenant: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def view_tenants():
    """View all tenants with their appartement info"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT t.id, t.name, t.phone, 
                   h.house_number, h.rent
            FROM tenants t
            JOIN houses h ON t.house_id = h.id
            ORDER BY t.name
        """)
        return cur.fetchall()
    except Exception as e:
        print(f"Error viewing tenants: {e}")
        return []
    finally:
        conn.close()

def delete_tenant(tenant_id):
    """Delete a tenant and mark appartement as vacant"""
    conn = connect()
    cur = conn.cursor()
    try:
        # Get house_id before deletion
        cur.execute("SELECT house_id FROM tenants WHERE id = ?", (tenant_id,))
        result = cur.fetchone()
        if not result:
            return False
            
        house_id = result[0]
        
        # Delete tenant
        cur.execute("DELETE FROM tenants WHERE id = ?", (tenant_id,))
        
        # Mark appartement as vacant
        update_house_status(house_id, 'vacant')
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting tenant: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_tenant_by_name(name):
    """Search for tenants by name (for payment processing)"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT t.id, t.name, h.house_number, h.rent
            FROM tenants t
            JOIN houses h ON t.house_id = h.id
            WHERE t.name LIKE ?
        """, (f"%{name}%",))
        return cur.fetchall()
    except Exception as e:
        print(f"Error finding tenant: {e}")
        return []
    finally:
        conn.close()

def get_tenant_by_id(tenant_id):
    """Get single tenant details"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT t.id, t.name, t.phone, h.house_number, h.rent
            FROM tenants t
            JOIN houses h ON t.house_id = h.id
            WHERE t.id = ?
        """, (tenant_id,))
        return cur.fetchone()
    except Exception as e:
        print(f"Error getting tenant: {e}")
        return None
    finally:
        conn.close()