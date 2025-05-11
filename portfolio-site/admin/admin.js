// Admin API endpoints
const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');

// Mock admin credentials (in production, use a proper database)
const ADMIN_CREDENTIALS = {
  email: "admin@illaiproduction.com",
  password: "securePassword123"
};

// Login endpoint
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  
  if (email === ADMIN_CREDENTIALS.email && password === ADMIN_CREDENTIALS.password) {
    const token = jwt.sign(
      { email, role: 'admin' },
      process.env.JWT_SECRET || 'your_jwt_secret_key',
      { expiresIn: '1h' }
    );
    
    res.json({
      success: true,
      token,
      redirect: '/admin/dashboard'
    });
  } else {
    res.status(401).json({
      success: false,
      message: 'Invalid credentials'
    });
  }
});

// Protected route example
router.get('/dashboard', authenticateToken, (req, res) => {
  res.json({
    success: true,
    data: {
      stats: {
        visitors: 1243,
        conversions: 42,
        revenue: 12500
      }
    }
  });
});

// Authentication middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) return res.sendStatus(401);
  
  jwt.verify(token, process.env.JWT_SECRET || 'your_jwt_secret_key', (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

module.exports = router;