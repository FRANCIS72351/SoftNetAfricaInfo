# SoftNet Africa - Modern Course Platform

## ✨ New Features Implemented

### 1. **Responsive Design** ✅
- Mobile-first design using Tailwind CSS
- Adapts beautifully to all screen sizes (mobile, tablet, desktop)
- Sticky navigation bar with smooth interactions
- Touch-friendly buttons and forms

### 2. **Dark Mode Toggle** ✅
- Automatic detection of system preference
- Manual toggle button in navigation
- Persistent theme storage in localStorage
- Smooth transitions between themes

### 3. **Course Search & Filtering** ✅
- Real-time search bar in the navigation
- Filter courses by title, duration, days, or time
- Instant visual feedback

### 4. **Modern UI/UX** ✅
- Beautiful gradient headers
- Card-based course layout with hover effects
- Improved typography and spacing
- Professional color scheme (blue primary, slate neutrals)
- Icons from modern SVG graphics

### 5. **Database-Driven Courses** ✅
- Courses stored in SQLite database
- No need to edit code to manage courses
- Dynamic data loading
- Scalable architecture

### 6. **Admin Dashboard** ✅
- Secure login with password protection
- Manage courses (Add, Edit, Delete)
- View all student inquiries in real-time
- Dashboard statistics (total courses, inquiries count)
- Clean admin interface with dark mode support

### 7. **Contact/Inquiry Form** ✅
- Modern form with validation
- Client-side and server-side validation
- Stores inquiries in database
- Visible in admin panel with timestamps

### 8. **Social Sharing** ✅
- WhatsApp, Twitter, Facebook sharing buttons
- Direct link copying
- Custom share text

### 9. **Modern Icons & Animations** ✅
- SVG-based icons throughout
- Hover animations on cards
- Smooth transitions and effects
- Loading states (ready for enhancement)

---

## 🚀 How to Use

### Running the Application
```bash
python main.py
```
The app will run at `http://localhost:5000`

### Admin Access
- Go to `http://localhost:5000/admin/login`
- Default password: `admin123` ⚠️ **Change this in production!**
- From admin panel, you can:
  - Add new courses
  - Edit existing courses
  - Delete courses
  - View all student inquiries

### Files Structure
```
information_sheet/
├── main.py                          # Flask backend
├── courses.db                       # Database (auto-created)
├── shortlink_db.py                  # URL shortening module
├── shortlinks.db                    # Short link database
└── static/image/template/
    ├── index.html                   # Main public page
    ├── admin.html                   # Admin dashboard
    └── admin_login.html             # Admin login page
```

---

## 🔒 Security Notes

1. **Change the secret key** in `main.py` line 9:
   ```python
   app.secret_key = 'your-secret-key-change-this'
   ```

2. **Change the admin password** in `main.py` line 135:
   ```python
   if password == 'admin123':  # Change 'admin123' to something secure
   ```

3. In production, consider:
   - Using environment variables for secrets
   - Implementing rate limiting
   - Adding CSRF protection
   - Using HTTPS
   - Implementing proper authentication

---

## 🎨 Customization

### Colors
Edit the color scheme in `index.html` and `admin.html` by changing Tailwind color classes:
- Primary: `blue-600` (currently)
- Secondary: `slate-*` (neutral grays)

### Database Path
The database is stored as `courses.db` in the root directory. To use a different location, modify `main.py` line 13:
```python
DB_PATH = "courses.db"
```

### Logo/Image Path
Change the image path in the database or at runtime:
```python
"image_path": "static/img/hdjjssw.jpg"
```

---

## 📦 Dependencies

- **Flask** - Web framework
- **Tailwind CSS** - Styling (loaded via CDN)
- **SQLite** - Database (built-in with Python)

No additional npm packages needed! Everything is built with vanilla Python and HTML/CSS/JS.

---

## 📝 API Endpoints

### Public Routes
- `GET /` - Main page
- `POST /contact` - Submit inquiry form
- `GET /r/<code>` - Redirect short link

### Admin Routes
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Authenticate
- `GET /admin` - Admin dashboard
- `GET /admin/logout` - Logout

### Admin API Routes
- `POST /api/course` - Add new course
- `PUT /api/course/<id>` - Edit course
- `DELETE /api/course/<id>` - Delete course

---

## ✅ Quality Checklist

- ✅ Fully responsive design
- ✅ Dark mode support
- ✅ Search functionality
- ✅ Database integration
- ✅ Admin dashboard
- ✅ Contact form with storage
- ✅ Modern UI/UX
- ✅ No external dependencies (except Tailwind CDN)
- ✅ Clean, maintainable code
- ✅ Professional appearance

---

**Enjoy your modern, feature-rich course platform! 🎉**
