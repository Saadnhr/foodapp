"""
Quick Diagnostic - Check what files are missing
"""
import os

def check_files():
    print("=" * 60)
    print("FILE STRUCTURE DIAGNOSTIC")
    print("=" * 60)
    print(f"\nCurrent directory: {os.getcwd()}\n")
    
    # Check templates folder
    print("TEMPLATES FOLDER:")
    if os.path.exists('templates'):
        print("✅ templates/ folder exists")
        templates = os.listdir('templates')
        print(f"   Found {len(templates)} files:")
        for t in sorted(templates):
            print(f"   - {t}")
    else:
        print("❌ templates/ folder DOES NOT EXIST")
        print("   You need to create this folder and add HTML files!")
    
    print("\n" + "-" * 60 + "\n")
    
    # Check static folder
    print("STATIC FOLDER:")
    if os.path.exists('static'):
        print("✅ static/ folder exists")
        if os.path.exists('static/css'):
            css_files = os.listdir('static/css')
            print(f"   CSS files: {css_files}")
        else:
            print("   ❌ static/css/ folder missing")
        
        if os.path.exists('static/js'):
            js_files = os.listdir('static/js')
            print(f"   JS files: {js_files}")
        else:
            print("   ❌ static/js/ folder missing")
    else:
        print("❌ static/ folder DOES NOT EXIST")
        print("   You need to create this folder and add CSS/JS files!")
    
    print("\n" + "=" * 60)
    print("REQUIRED FILES:")
    print("=" * 60)
    
    required_templates = [
        'base.html', 'index.html', 'login.html', 'register.html',
        'dashboard_company.html', 'dashboard_volunteer.html', 
        'add_donation.html', 'about.html', '404.html', '500.html'
    ]
    
    print("\nTemplates needed in templates/ folder:")
    for template in required_templates:
        exists = os.path.exists(f'templates/{template}')
        status = "✅" if exists else "❌"
        print(f"  {status} {template}")
    
    print("\nStatic files needed:")
    css_exists = os.path.exists('static/css/style.css')
    js_exists = os.path.exists('static/js/scripts.js')
    print(f"  {'✅' if css_exists else '❌'} static/css/style.css")
    print(f"  {'✅' if js_exists else '❌'} static/js/scripts.js")
    
    print("\n" + "=" * 60)
    print("WHAT TO DO:")
    print("=" * 60)
    
    if not os.path.exists('templates'):
        print("\n1. CREATE templates folder:")
        print("   mkdir templates")
        print("\n2. COPY all .html files into templates/")
        print("   (You should have downloaded them from Claude)")
    elif len(os.listdir('templates')) < 10:
        print("\n1. You have templates/ folder but missing files!")
        print("   Need to copy all HTML files from downloaded folder")
    
    if not os.path.exists('static'):
        print("\n3. CREATE static folders:")
        print("   mkdir static")
        print("   mkdir static\\css")
        print("   mkdir static\\js")
        print("\n4. COPY CSS and JS files:")
        print("   - style.css → static/css/")
        print("   - scripts.js → static/js/")
    
    print("\n" + "=" * 60)
    print("\nAll files should be in the folder you downloaded from Claude.")
    print("Look for a folder on your Desktop or Downloads with these files!")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    check_files()
    input("\nPress Enter to exit...")