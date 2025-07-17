"""
Logo Component - 3D ORGMASTER banner logo with enhanced visual effects
"""

import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter


class AnimatedLogo:
    """3D ORGMASTER banner logo with enhanced visual effects"""
    
    def __init__(self, parent, logo_path="logo.png", size=(250, 60)):
        self.parent = parent
        self.size = size
        self.animation_enabled = True
        
        # Enhanced canvas for 3D effects with proper sizing to prevent cutoff
        self.canvas = tk.Canvas(
            parent, 
            width=size[0] + 40,  # Increased padding to prevent cutoff
            height=size[1] + 25, # Increased padding to prevent cutoff
            highlightthickness=0, 
            bd=0,
            relief='flat'
        )
        self.canvas.pack(side=tk.LEFT, padx=(5, 20), pady=5)  # Reduced left padding
        
        # Load and display 3D banner logo
        self.original_image = self._load_3d_banner_logo(logo_path)
        self._display_3d_banner()
        
        if self.animation_enabled:
            self._start_animation()
    
    def _load_3d_banner_logo(self, logo_path):
        """Load and create 3D ORGMASTER banner logo"""
        # Try to load existing image first
        possible_paths = [
            logo_path,
            "logo.png",
            "banner.png",
            "orgmaster_banner.png",
            "assets/logo.png"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize(self.size, Image.Resampling.LANCZOS)
                    return self._apply_3d_effects(img)
                except Exception as e:
                    print(f"Error loading banner from {path}: {e}")
                    continue
        
        return self._create_3d_orgmaster_banner()
    
    def _create_3d_orgmaster_banner(self):
        """Create professional 3D ORGMASTER banner with Monokai colors"""
        working_size = (self.size[0] + 20, self.size[1] + 20)
        img = Image.new('RGBA', working_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Monokai color scheme for logo
        primary_color = (39, 40, 34)       # Monokai background #272822
        highlight_color = (102, 217, 239)   # Monokai cyan #66D9EF
        shadow_color = (30, 31, 28)        # Darker monokai
        accent_color = (253, 151, 31)       # Monokai orange #FD971F
        text_color = (248, 248, 242)        # Monokai foreground #F8F8F2
        
        corner_radius = 20
        base_rect = (10, 10, working_size[0] - 10, working_size[1] - 10)
        
        # Bottom shadow layer with Monokai colors
        shadow_rect = (base_rect[0] + 3, base_rect[1] + 3, base_rect[2] + 3, base_rect[3] + 3)
        draw.rounded_rectangle(shadow_rect, radius=corner_radius, fill=(*shadow_color, 180))
        
        # Main 3D body with Monokai background
        draw.rounded_rectangle(base_rect, radius=corner_radius, fill=primary_color)
        
        # Create 3D gradient effect with Monokai colors
        self._create_3d_gradient(draw, base_rect, primary_color, highlight_color, corner_radius)
        
        # Add enhanced 3D beveled edges
        self._add_3d_bevel_effects(draw, base_rect, corner_radius)
        
        # Add Monokai-themed typography
        self._add_monokai_text(draw, base_rect, text_color, accent_color)
        
        # Add Monokai logo elements
        self._add_monokai_logo_elements(draw, base_rect, accent_color, highlight_color)
        
        # Apply final rounded corner mask
        final_img = self._apply_rounded_corners_mask(img, corner_radius, working_size)
        final_img = final_img.crop((10, 10, working_size[0] - 10, working_size[1] - 10))
        
        return final_img

    def _apply_rounded_corners_mask(self, img, corner_radius, size):
        """Apply rounded corners mask to the entire image"""
        # Create a mask for rounded corners
        mask = Image.new('L', size, 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Draw rounded rectangle on mask
        mask_draw.rounded_rectangle(
            (10, 10, size[0] - 10, size[1] - 10), 
            radius=corner_radius, 
            fill=255
        )
        
        # Apply the mask to create rounded corners
        rounded_img = Image.new('RGBA', size, (0, 0, 0, 0))
        rounded_img.paste(img, (0, 0))
        rounded_img.putalpha(mask)
        
        return rounded_img

    def _add_3d_bevel_effects(self, draw, rect, corner_radius):
        """Add 3D beveled edges for depth with rounded corners"""
        x1, y1, x2, y2 = rect
        
        # Top and left highlight edges with rounded corners
        highlight_color = (255, 255, 255, 120)
        
        # Enhanced top edge highlight with rounded corners
        for i in range(4):  # Increased layers for better effect
            highlight_rect = (x1 + i, y1 + i, x2 - i, y1 + i + 2)
            draw.rounded_rectangle(
                highlight_rect,
                radius=max(1, corner_radius - i),
                outline=highlight_color,
                width=1
            )
        
        # Enhanced left edge highlight
        for i in range(4):
            draw.line([(x1 + i, y1 + corner_radius), (x1 + i, y2 - corner_radius)], 
                     fill=highlight_color, width=1)
        
        # Bottom and right shadow edges with rounded corners
        shadow_color = (0, 0, 0, 100)  # Slightly darker for better contrast
        
        # Enhanced bottom edge shadow with rounded corners
        for i in range(3):
            shadow_rect = (x1 + corner_radius, y2 - i - 2, x2 - corner_radius, y2 - i - 1)
            draw.rectangle(shadow_rect, fill=shadow_color)
        
        # Enhanced right edge shadow
        for i in range(3):
            draw.line([(x2 - i - 2, y1 + corner_radius), (x2 - i - 2, y2 - corner_radius)], 
                     fill=shadow_color, width=1)
        
        # Add corner highlights for 3D effect
        self._add_corner_highlights(draw, rect, corner_radius, highlight_color, shadow_color)

    def _add_corner_highlights(self, draw, rect, corner_radius, highlight_color, shadow_color):
        """Add corner highlights and shadows for enhanced 3D effect"""
        x1, y1, x2, y2 = rect
        
        # Top-left corner highlight (brightest)
        for i in range(3):
            draw.arc(
                (x1 + i, y1 + i, x1 + corner_radius * 2 - i, y1 + corner_radius * 2 - i),
                start=180, end=270,
                fill=highlight_color, width=2
            )
        
        # Top-right corner highlight
        for i in range(2):
            draw.arc(
                (x2 - corner_radius * 2 + i, y1 + i, x2 - i, y1 + corner_radius * 2 - i),
                start=270, end=360,
                fill=(255, 255, 255, 80), width=1
            )
        
        # Bottom-right corner shadow (darkest)
        for i in range(3):
            draw.arc(
                (x2 - corner_radius * 2 + i, y2 - corner_radius * 2 + i, x2 - i, y2 - i),
                start=0, end=90,
                fill=shadow_color, width=2
            )
        
        # Bottom-left corner shadow
        for i in range(2):
            draw.arc(
                (x1 + i, y2 - corner_radius * 2 + i, x1 + corner_radius * 2 - i, y2 - i),
                start=90, end=180,
                fill=(0, 0, 0, 60), width=1
            )

    def _apply_3d_effects(self, img):
        """Apply 3D effects to existing image with rounded corners"""
        # Resize to exact dimensions first
        img = img.resize(self.size, Image.Resampling.LANCZOS)
        
        # Apply rounded corners to existing images
        corner_radius = 20
        
        # Create mask for rounded corners
        mask = Image.new('L', self.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            (0, 0, self.size[0], self.size[1]), 
            radius=corner_radius, 
            fill=255
        )
        
        # Apply the mask
        rounded_img = Image.new('RGBA', self.size, (0, 0, 0, 0))
        rounded_img.paste(img, (0, 0))
        rounded_img.putalpha(mask)
        
        # Add subtle 3D enhancement
        enhanced = rounded_img.copy()
        
        # Apply slight blur for depth while preserving rounded corners
        blurred = enhanced.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Combine for subtle 3D effect
        final_img = Image.blend(enhanced, blurred, 0.2)
        
        # Add subtle drop shadow effect
        shadow_img = self._add_drop_shadow(final_img, corner_radius)
        
        return shadow_img

    def _add_drop_shadow(self, img, corner_radius):
        """Add a subtle drop shadow to the rounded logo"""
        # Create shadow
        shadow_size = (img.width + 6, img.height + 6)
        shadow = Image.new('RGBA', shadow_size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw shadow with rounded corners
        shadow_draw.rounded_rectangle(
            (3, 3, shadow_size[0] - 3, shadow_size[1] - 3),
            radius=corner_radius,
            fill=(0, 0, 0, 40)  # Semi-transparent black
        )
        
        # Blur the shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Create final image with shadow
        final_img = Image.new('RGBA', shadow_size, (0, 0, 0, 0))
        final_img.paste(shadow, (0, 0))
        final_img.paste(img, (3, 3), img)
        
        # Resize back to original size
        final_img = final_img.resize(self.size, Image.Resampling.LANCZOS)
        
        return final_img

    def _display_3d_banner(self):
        """Display the 3D banner with enhanced effects and proper centering"""
        self.photo = ImageTk.PhotoImage(self.original_image)
        
        # Calculate center position with proper padding to prevent cutoff
        canvas_width = self.size[0] + 40  # Match the canvas width
        canvas_height = self.size[1] + 25  # Match the canvas height
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Create image at center with proper positioning
        self.canvas.create_image(center_x, center_y, image=self.photo, anchor="center")
    
    def _start_animation(self):
        """Enhanced animation for 3D logo"""
        self.parent.after(100, self._animate_3d_step)
    
    def _animate_3d_step(self):
        """3D animation step with subtle effects"""
        if self.animation_enabled:
            # Subtle pulsing effect for 3D logo
            self.parent.after(3000, self._animate_3d_step)
    
    def _add_monokai_text(self, draw, rect, text_color, accent_color):
        """Add Monokai-themed text to the logo"""
        x1, y1, x2, y2 = rect
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        try:
            # Try to load a font
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Main text with Monokai foreground color
        text = "ORGANIZER"
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw text shadow first (darker)
        shadow_offset = 2
        draw.text(
            (center_x - text_width//2 + shadow_offset, center_y - text_height//2 + shadow_offset),
            text, 
            fill=(0, 0, 0, 120),
            font=font
        )
        
        # Draw main text in Monokai foreground color
        draw.text(
            (center_x - text_width//2, center_y - text_height//2),
            text, 
            fill=text_color,
            font=font
        )

    def _add_monokai_logo_elements(self, draw, rect, accent_color, highlight_color):
        """Add Monokai-themed decorative elements"""
        x1, y1, x2, y2 = rect
        
        # Add small accent dots in Monokai colors
        dot_size = 3
        
        # Orange accent dots
        draw.ellipse(
            (x1 + 15, y1 + 15, x1 + 15 + dot_size, y1 + 15 + dot_size),
            fill=accent_color
        )
        
        # Cyan accent dots
        draw.ellipse(
            (x2 - 15 - dot_size, y1 + 15, x2 - 15, y1 + 15 + dot_size),
            fill=highlight_color
        )

    def update_theme(self, is_dark_mode):
        """Update theme for Monokai logo"""
        # Monokai theme colors
        if is_dark_mode:
            bg_color = "#272822"  # Monokai background
        else:
            bg_color = "#FAFAFA"  # Light background
            
        self.canvas.configure(bg=bg_color)
        
        try:
            self.parent.configure(bg=bg_color)
        except:
            pass