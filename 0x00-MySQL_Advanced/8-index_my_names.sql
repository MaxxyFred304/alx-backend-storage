-- Assuming the table 'names' already exists

-- Create the index
CREATE INDEX idx_name_first ON names (LEFT(name, 1));

