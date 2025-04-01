package com.argusai.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "image_analysis")
public class ImageAnalysis {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fileName;
    private String analysisType; // "OBJECT_DETECTION" or "GENERAL_ANALYSIS"
    private String targetObject; // For object detection
    private String result;
    private LocalDateTime createdAt;
} 