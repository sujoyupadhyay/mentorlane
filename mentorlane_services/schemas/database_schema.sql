-- Create teaching_modes table
CREATE TABLE IF NOT EXISTS teaching_modes (
    teaching_mode_id VARCHAR(36) NOT NULL DEFAULT (UUID()),
    teaching_mode VARCHAR(20) NOT NULL,
    IsActive TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (teaching_mode_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data
INSERT INTO teaching_modes (teaching_mode_id, teaching_mode, IsActive) VALUES
(UUID(), 'Online', 1),
(UUID(), 'In-Person', 1),
(UUID(), 'Hybrid', 1),
(UUID(), 'Recorded', 0),
(UUID(), 'Live', 1);

-- Create teaching_languages table
CREATE TABLE IF NOT EXISTS teaching_languages (
    teaching_languages_id VARCHAR(36) NOT NULL DEFAULT (UUID()),
    teaching_language VARCHAR(20) NOT NULL,
    IsActive TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (teaching_languages_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert sample data
INSERT INTO teaching_languages (teaching_languages_id, teaching_language, IsActive) VALUES
(UUID(), 'English', 1),
(UUID(), 'Bengali', 1),
(UUID(), 'Hindi', 1),
(UUID(), 'Kannada', 0),
(UUID(), 'Tamil', 1);

-- Create teaching_levels table
CREATE TABLE IF NOT EXISTS teaching_levels (
    teaching_levels_id VARCHAR(36) NOT NULL DEFAULT (UUID()),
    teaching_level_name VARCHAR(20) NOT NULL,
    teaching_level_description VARCHAR(200) NOT NULL,
    IsActive TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (teaching_levels_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert sample data
INSERT INTO teaching_levels (teaching_levels_id, teaching_level_name, teaching_level_description, IsActive) VALUES
(UUID(), 'Beginner', 'Introductory level for beginners', 1),
(UUID(), 'Intermediate', 'Intermediate level for learners with some experience', 1),
(UUID(), 'Advanced', 'Advanced level for experienced learners', 1),
(UUID(), 'Expert', 'Expert level for professionals', 0),
(UUID(), 'All Levels', 'Suitable for all proficiency levels', 1);
