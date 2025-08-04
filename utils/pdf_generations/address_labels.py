import json
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import gray, black
from utils.get_data_file import get_data_file
from utils.open_file_in_preview import open_file_in_preview

def generate_address_labels():
    # Open file dialog to let the user choose where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save PDF As",
        initialfile="address_labels.pdf"
    )
    
    if not file_path:  # If user cancels, stop execution
        return

    # Create canvas
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Avery 5160 label specifications
    # Page margins
    left_margin = 0.1875 * inch  # 3/16 inch
    top_margin = 0.5 * inch      # 1/2 inch
    
    # Label dimensions
    label_width = 2.625 * inch   # 2 5/8 inches
    label_height = 1.0 * inch    # 1 inch
    
    # Spacing between labels
    horizontal_spacing = 0.125 * inch  # 1/8 inch
    vertical_spacing = 0.0 * inch      # No vertical spacing
    
    # Number of labels per row and column
    labels_per_row = 3
    labels_per_column = 10
    
    # Get Student Data
    with open(get_data_file('data/class_demo.txt'), 'r') as file:
        content = file.read()
        student_demo_json = json.loads(content)
    
    # Collect all addresses
    addresses = []
    for student_id, student_data in student_demo_json.items():
        contact_one = student_data.get('contact_one')
        if contact_one and contact_one.get('name'):
            # Format the address
            name = contact_one['name']
            street = student_data.get('street', '')
            city = student_data.get('city', '')
            state = student_data.get('state', '')
            zip_code = student_data.get('zip', '')
            
            # Create address lines
            address_lines = [
                name,
                street,
                f"{city}, {state} {zip_code}"
            ]
            
            addresses.append(address_lines)
    
    # Calculate how many pages we need
    labels_per_page = labels_per_row * labels_per_column
    total_pages = (len(addresses) + labels_per_page - 1) // labels_per_page
    
    # Generate labels
    for page in range(total_pages):
        if page > 0:
            c.showPage()
        
        # Add Avery format indicator in top-right corner
        c.setFont("Helvetica", 8)
        c.setFillColor(gray)
        format_text = "Avery 5160 (1\" x 2 5/8\")"
        text_width = c.stringWidth(format_text, "Helvetica", 8)
        c.drawString(width - text_width - 10, height - 15, format_text)
        c.setFillColor(black)  # Reset to black
        
        for label_index in range(labels_per_page):
            address_index = (page * labels_per_page) + label_index
            
            if address_index >= len(addresses):
                break
            
            # Calculate position on the page
            row = label_index // labels_per_row
            col = label_index % labels_per_row
            
            # Calculate label position
            x = left_margin + col * (label_width + horizontal_spacing)
            y = height - top_margin - (row + 1) * (label_height + vertical_spacing)
            
            # Get the address for this label
            address_lines = addresses[address_index]
            
            # Set font
            c.setFont("Helvetica", 10)
            
            # Draw address lines
            line_height = 12  # Points between lines
            for i, line in enumerate(address_lines):
                if line.strip():  # Only draw non-empty lines
                    text_y = y + label_height - (20 + i * line_height)
                    c.drawString(x + 5, text_y, line)
            
            # Optional: Draw border around each label for debugging
            # Uncomment the next line to see label boundaries
            # c.rect(x, y, label_width, label_height)
    
    # Save the PDF file
    c.save()
    
    open_file_in_preview(file_path)
