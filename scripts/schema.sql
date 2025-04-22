-- Users table to store user information
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Conversations table to store conversation sessions
CREATE TABLE IF NOT EXISTS conversations (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    status VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    metadata JSON,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Messages table to store all messages in conversations
CREATE TABLE IF NOT EXISTS messages (
    id CHAR(36) PRIMARY KEY,
    conversation_id CHAR(36),
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_metadata JSON,
    tokens_used INTEGER,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Affidavits table to store generated affidavits
CREATE TABLE IF NOT EXISTS affidavits (
    id CHAR(36) PRIMARY KEY,
    conversation_id CHAR(36),
    content TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    approved_by CHAR(36),
    approved_at TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Timeline_events table to store extracted timeline events
CREATE TABLE IF NOT EXISTS timeline_events (
    id CHAR(36) PRIMARY KEY,
    conversation_id CHAR(36),
    event_date TIMESTAMP,
    description TEXT NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_message_id CHAR(36),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (source_message_id) REFERENCES messages(id)
);

-- Evidence table to store references to evidence
CREATE TABLE IF NOT EXISTS evidence (
    id CHAR(36) PRIMARY KEY,
    conversation_id CHAR(36),
    type VARCHAR(50) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

-- Indexes for better query performance
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_affidavits_conversation_id ON affidavits(conversation_id);
CREATE INDEX idx_timeline_events_conversation_id ON timeline_events(conversation_id);
CREATE INDEX idx_evidence_conversation_id ON evidence(conversation_id);
