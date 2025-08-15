from utils.db import connect

def add_house(appartement_number, location, rent):
    """Add a new appartement to the database"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO houses (house_number, location, rent, status)
            VALUES (?, ?, ?, 'vacant')
        """, (appartement_number, location, rent))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding appartement: {e}")
        return False
    finally:
        conn.close()

def view_houses():
    """View all appartements with their current status"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, house_number, location, rent, status 
            FROM houses
            ORDER BY house_number
        """)
        return cur.fetchall()
    except Exception as e:
        print(f"Error viewing appartements: {e}")
        return []
    finally:
        conn.close()

def update_house_rent(house_id, new_rent):
    """Update the rent amount for an appartement"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE houses 
            SET rent = ?
            WHERE id = ?
        """, (new_rent, house_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error updating appartement rent: {e}")
        return False
    finally:
        conn.close()

def delete_house(house_id):
    """Delete an appartement from the system"""
    conn = connect()
    cur = conn.cursor()
    try:
        # First delete any tenants in this appartement
        cur.execute("DELETE FROM tenants WHERE house_id = ?", (house_id,))
        # Then delete the appartement
        cur.execute("DELETE FROM houses WHERE id = ?", (house_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error deleting appartement: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_vacant_houses():
    """Get only vacant appartements for tenant assignment"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, house_number, rent 
            FROM houses 
            WHERE status = 'vacant'
            ORDER BY house_number
        """)
        return cur.fetchall()
    except Exception as e:
        print(f"Error getting vacant appartements: {e}")
        return []
    finally:
        conn.close()

def update_house_status(house_id, status):
    """Update occupancy status of an appartement (vacant/occupied)"""
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE houses 
            SET status = ?
            WHERE id = ?
        """, (status, house_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error updating appartement status: {e}")
        return False
    finally:
        conn.close()