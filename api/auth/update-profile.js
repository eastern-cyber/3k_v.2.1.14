// api/auth/update-profile.js
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');

// Initialize pool
let pool;
try {
  pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
  });
} catch (error) {
  console.error('Database pool error:', error);
}

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  if (req.method !== 'PUT') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }
  
  try {
    // Get token
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ 
        success: false, 
        message: 'Access token required' 
      });
    }
    
    // Verify token
    const user = await new Promise((resolve, reject) => {
      jwt.verify(token, process.env.JWT_SECRET || 'development-secret', (err, user) => {
        if (err) reject(err);
        else resolve(user);
      });
    });
    
    const { name } = req.body;
    const userId = user.userId;
    
    // Validate
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Valid name is required'
      });
    }
    
    if (!pool) {
      return res.status(500).json({
        success: false,
        message: 'Database connection not available'
      });
    }
    
    // Update user
    const trimmedName = name.trim();
    const result = await pool.query(
      'UPDATE users SET name = $1 WHERE id = $2 RETURNING id, user_id, email, name',
      [trimmedName, userId]
    );
    
    if (result.rowCount === 0) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Profile updated successfully',
      user: result.rows[0]
    });
    
  } catch (error) {
    console.error('Update profile error:', error);
    
    if (error.name === 'JsonWebTokenError') {
      return res.status(403).json({
        success: false,
        message: 'Invalid token'
      });
    }
    
    res.status(500).json({
      success: false,
      message: 'Server error updating profile',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
};