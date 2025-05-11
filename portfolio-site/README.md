# iLL AI Music Video Production

Professional AI-powered music video production service.

## Deployment Instructions

1. **Netlify Setup**:
   ```bash
   # Install Netlify CLI if needed
   npm install -g netlify-cli

   # Login to Netlify
   netlify login

   # Deploy to Netlify
   netlify deploy --prod
   ```

2. **Environment Variables**:
   - Set these in Netlify dashboard:
     - `CONTACT_FORM_RECIPIENT`: Your email for form submissions
     - `ADMIN_PASSWORD`: Password for admin area (hashed)

3. **Features**:
   - Static site hosting
   - Form handling
   - Admin authentication
   - SEO optimized
   - Responsive design

4. **Custom Domains**:
   - Configure in Netlify dashboard
   - Set up DNS records as instructed

## Development

```bash
# Live preview (port 8000)
python3 -m http.server 8000
```

## Project Structure

```
portfolio-site/
├── assets/          # CSS and images
├── components/      # Reusable components
├── admin/           # Admin interface
└── *.html           # Main pages