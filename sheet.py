from mcp.server.fastmcp import FastMCP
from sheets_functions import (
    get_all_reservations,
    add_reservation,
    update_reservation,
    delete_reservation,
    DEFAULT_SPREADSHEET,
    DEFAULT_WORKSHEET
)

mcp = FastMCP("Google Sheets Reservation MCP") # Updated MCP name

@mcp.tool()
def get_reservations(random_string=""):
    """
    Gets reservations from the spreadsheet. Can filter by customer_name.

    :param random_string: Dummy parameter for no-parameter tools
    :return: A string containing the result of the fetch operation (list of reservations or error message).
    """

 
        # Sabit veri döndürelim (test amacıyla)
    result = get_all_reservations()
    return str(result)


@mcp.tool()
def add_new_reservation(customer_name: str, check_in_date: str, check_out_date: str, adults: int, children: int, room_type: str):
    """
    Adds a new reservation to the spreadsheet.

    :param customer_name: Name of the customer
    :param check_in_date: Check-in date (YYYY-MM-DD)
    :param check_out_date: Check-out date (YYYY-MM-DD)
    :param adults: Number of adults
    :param children: Number of children
    :param room_type: Type of room (e.g., Standard, Suite)
    :return: A string confirming the reservation addition or an error message.
    """
    try:
        # Gelen parametrelerden bir sözlük oluştur
        reservation_data = {
            "customer_name": customer_name,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": adults,
            "children": children,
            "room_type": room_type
            # Diğer potansiyel alanlar (varsa sheets_functions.py içindeki add_reservation'a göre eklenebilir)
            # Örneğin: "status": "Confirmed", "price": 0 
        }
        
        # add_reservation fonksiyonunu reservation_data sözlüğü ile çağır
        result = add_reservation(reservation_data=reservation_data)
        return str(result)
    except Exception as e:
        return f"Error adding reservation: {e}"


@mcp.tool()
def update_existing_reservation(reservation_id: str, customer_name: str = None, check_in_date: str = None, 
                               check_out_date: str = None, adults: int = None, children: int = None, room_type: str = None):
    """
    Updates an existing reservation in the spreadsheet.

    :param reservation_id: ID of the reservation to update
    :param customer_name: Name of the customer (optional)
    :param check_in_date: Check-in date (YYYY-MM-DD) (optional)
    :param check_out_date: Check-out date (YYYY-MM-DD) (optional)
    :param adults: Number of adults (optional)
    :param children: Number of children (optional)
    :param room_type: Type of room (e.g., Standard, Suite) (optional)
    :return: A string confirming the reservation update or an error message.
    """
    try:
        # Boş olmayan parametrelerden bir sözlük oluştur
        update_data = {}
        if customer_name is not None:
            update_data["customer_name"] = customer_name
        if check_in_date is not None:
            update_data["check_in_date"] = check_in_date
        if check_out_date is not None:
            update_data["check_out_date"] = check_out_date
        if adults is not None:
            update_data["adults"] = adults
        if children is not None:
            update_data["children"] = children
        if room_type is not None:
            update_data["room_type"] = room_type
        
        # Güncellenecek hiçbir alan yoksa kullanıcıyı bilgilendir
        if not update_data:
            return "No fields to update were provided. Please specify at least one field to update."
        
        # update_reservation fonksiyonunu çağır
        result = update_reservation(reservation_id=reservation_id, update_data=update_data)
        return str(result)
    except Exception as e:
        return f"Error updating reservation: {e}"


@mcp.tool()
def delete_existing_reservation(reservation_id: str = None, customer_name: str = None, room_type: str = None, use_customer_name: bool = False):
    """
    Tablodaki bir rezervasyonu siler.

    :param reservation_id: Silinecek rezervasyonun ID'si
    :param customer_name: Rezervasyonları silinecek müşteri adı
    :param room_type: Oda tipi (müşteri adına göre filtreleme yaparken kullanılır)
    :param use_customer_name: Kullanımdan kaldırılmıştır. Geriye dönük uyumluluk için korunmuştur.
    :return: Rezervasyon silme işleminin sonucunu veya hata mesajını içeren bir metin.
    """
    try:
        # Parametrelerin doğruluğunu kontrol et
        if reservation_id is None and customer_name is None:
            return "Hata: Rezervasyon silmek için rezervasyon ID veya müşteri adı belirtilmelidir."
            
        # customer_name parametresi veya use_customer_name=True ile çağrıldıysa müşteri adına göre sil
        if customer_name is not None:
            # Doğrudan müşteri adıyla silme
            result = delete_reservation(customer_name=customer_name, room_type=room_type)
        elif use_customer_name and reservation_id is not None:
            # Geriye dönük uyumluluk için: use_customer_name=True durumunda reservation_id'yi müşteri adı olarak kullan
            result = delete_reservation(customer_name=reservation_id, room_type=room_type)
        else:
            # Rezervasyon ID'si ile silme
            result = delete_reservation(reservation_id=reservation_id)
        
        if result:
            if customer_name:
                return f"'{customer_name}' müşterisine ait rezervasyon(lar) başarıyla silindi."
            else:
                return f"'{reservation_id}' ID'li rezervasyon başarıyla silindi."
        else:
            if customer_name:
                return f"'{customer_name}' müşterisine ait rezervasyon bulunamadı veya silinemedi."
            else:
                return f"'{reservation_id}' ID'li rezervasyon bulunamadı veya silinemedi."
    except Exception as e:
        return f"Rezervasyon silinirken hata oluştu: {e}"


if __name__ == "__main__":
    print("Starting Google Sheets Reservation MCP") # Updated print message
    mcp.run(transport='stdio')
