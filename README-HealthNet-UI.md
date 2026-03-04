# HealthNet UI - Medical-Grade Design System

## Overview

HealthNet is an AI-powered preventive healthcare platform that leverages India's Digital Public Infrastructure (ABHA, DigiLocker, UPI) for seamless health management. This document outlines the redesigned UI following medical-grade design principles.

## Design Philosophy

### Medical-Grade Design Principles
- **Clean, Calm Light Theme**: White background with slate/teal accents
- **High Contrast Text**: WCAG AA compliance for accessibility
- **Generous Whitespace**: 8px spacing scale throughout
- **Responsive 12-Column Grid**: Consistent layout system
- **Card-Based Content**: All content blocks use consistent card styling
- **F-Pattern Scanning**: Most important KPIs at top-left, details lower

### Color Palette
```css
--primary-slate: #475569
--primary-teal: #0f766e
--accent-blue: #3b82f6
--success-green: #10b981
--warning-orange: #f59e0b
--danger-red: #ef4444
--text-primary: #1e293b
--text-secondary: #64748b
--bg-white: #ffffff
--bg-gray-50: #f8fafc
--border-gray: #e2e8f0
```

## Page Structure

### 1. Home Page (`index.html`)
**Hero Section**: Value proposition about India's DPI with "Connect ABHA" CTA
**Feature Cards**: Three main features (Records, Payments, AI Insights)
**Quick Actions**: Four action cards for immediate access
**Testimonials & Security**: Trust-building sections

### 2. Dashboard (`dashboard-new.html`)
**2-Row Responsive Grid**:
- **Row 1**: Four KPI cards (BP, Cholesterol, Glucose, BMI) + AI Risk card
- **Row 2**: Alerts & Reminders (2/3 width) + Latest Reports (1/3 width) + AI Recommendations (1/3 width)

**KPI Cards Include**:
- Current value with units
- Status badges (Normal/Elevated/High)
- Progress bars
- Last updated timestamps

### 3. Food Tracker (`food-tracker-new.html`)
**Left 2/3**: Today's Intake
- Daily summary with macro breakdown
- Progress bars for carbs, protein, fat, fiber
- Meals list with timestamps
- Nutrition insights and nudges

**Right 1/3**: Weekly Trends
- Simple bar charts for calories and protein
- Quick add food options

### 4. AI Health Scan (`ai-scan.html`)
**Hero Card**: "Run AI Scan" CTA with description
**Risk Assessment Cards**:
- Diabetes Risk (12.5% probability)
- Hypertension Risk (18.3% probability)
- Top contributing factors with impact levels
- SHAP-style factor tags

### 5. Prescription OCR (`ocr.html`)
**Upload Panel**: Drag-and-drop interface
**Split View Results**:
- Left: Extracted raw text
- Right: Parsed medications as chips
- "Save to Records" functionality

## Component Library

### Health Cards
```css
.health-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease-in-out;
}
```

### KPI Badges
```css
.kpi-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
}
```

### Progress Bars
```css
.progress-bar {
    width: 100%;
    height: 8px;
    background-color: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
}
```

## Navigation Structure

### Global Shell
- **Top Navbar**: Logo (left), Primary nav (center), Profile/alerts (right)
- **Optional Left Sidebar**: Quick actions on desktop
- **Mobile**: Collapsed sidebar, stacked cards

### Primary Navigation
1. Home
2. Dashboard
3. Food Tracker
4. Questionnaire
5. AI Scan
6. OCR

## API Integration Points

### Health Data
- `GET /api/health` - Ping for header status
- `POST /api/analyze-health` - Scan/Questionnaire results
- `POST /api/ocr/prescription` - OCR output
- `POST /api/chat` - Assistant functionality

### Data Flow
1. **Dashboard**: Loads KPI data and AI recommendations
2. **Food Tracker**: Tracks nutrition intake and trends
3. **AI Scan**: Analyzes health data for risk assessment
4. **OCR**: Processes prescription images

## Accessibility Features

### WCAG AA Compliance
- High contrast text (4.5:1 ratio minimum)
- Semantic HTML structure
- Focus states for keyboard navigation
- ARIA labels for screen readers
- Color-independent status indicators

### Mobile Responsiveness
- Responsive grid system
- Touch-friendly interface elements
- Optimized for F-pattern scanning
- Pinned primary CTAs

## Micro-Interactions

### Loading States
- Skeleton loaders for charts/cards
- Progress indicators for file uploads
- Smooth transitions between states

### Toast Notifications
- Success/error/warning messages
- Auto-dismiss after 3 seconds
- Non-intrusive positioning

### Form Validation
- Inline validation messages
- Real-time feedback
- Clear error states

## Implementation Guidelines

### Tailwind CSS Classes
- Use consistent spacing scale (8px increments)
- Leverage medical-grade color palette
- Implement responsive breakpoints
- Maintain consistent typography

### JavaScript Integration
- Modular component structure
- API error handling
- Loading state management
- Form validation

### Performance Considerations
- Lazy loading for charts
- Optimized images
- Minimal JavaScript bundle
- Fast initial page load

## File Structure

```
frontend/
├── index.html              # Home page
├── dashboard-new.html      # Main dashboard
├── food-tracker-new.html   # Nutrition tracking
├── ai-scan.html           # AI health analysis
├── ocr.html               # Prescription scanning
├── questionnaire.html     # Health assessment
├── js/
│   ├── health-api.js      # API integration
│   └── unified-nav.js     # Navigation logic
└── README-HealthNet-UI.md # This documentation
```

## Getting Started

1. **Install Dependencies**: Ensure Tailwind CSS is loaded
2. **Start Development**: Open `index.html` in a web browser
3. **API Setup**: Configure backend endpoints in `js/health-api.js`
4. **Customization**: Modify color palette and spacing as needed

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Future Enhancements

- Dark mode support
- Advanced charting library integration
- Real-time data updates
- Offline functionality
- PWA capabilities

## Contributing

When contributing to the HealthNet UI:

1. Follow the medical-grade design principles
2. Maintain WCAG AA accessibility standards
3. Use the established component library
4. Test across different screen sizes
5. Ensure consistent spacing and typography

## License

This project is part of the HealthNet preventive healthcare platform.
