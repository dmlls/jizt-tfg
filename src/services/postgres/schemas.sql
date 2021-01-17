/*
* Copyright (C) 2021 Diego Miguel Lozano <dml1001@alu.ubu.es>
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
* For license information on the libraries used, see LICENSE.
*/


/*
* DROP TYPES and TABLES
*/
DROP TYPE IF EXISTS NLP_TASK CASCADE;
DROP TYPE IF EXISTS STATUS CASCADE;

DROP TABLE IF EXISTS summary CASCADE;
DROP TABLE IF EXISTS model CASCADE;
DROP TABLE IF EXISTS model_family CASCADE;
DROP TABLE IF EXISTS vendor CASCADE;
DROP TABLE IF EXISTS language CASCADE;
DROP TABLE IF EXISTS source CASCADE;


/*
* CREATE TABLES
*/
CREATE TABLE source (
    source_id           SERIAL PRIMARY KEY,
    content             TEXT UNIQUE NOT NULL,
    content_length      INTEGER NOT NULL CHECK (content_length > 0)
);

CREATE TABLE language (
    language_id         SERIAL PRIMARY KEY,
    name                TEXT NOT NULL,
    language_tag        TEXT UNIQUE NOT NULL
);

CREATE TABLE vendor (
    vendor_id           SERIAL PRIMARY KEY,
    name                TEXT UNIQUE NOT NULL,
    see                 TEXT
);

CREATE TABLE model_family (
    family_id           SERIAL PRIMARY KEY,
    name                TEXT UNIQUE NOT NULL,
    authors             TEXT[],
    organizations       TEXT[],
    year                DATE,
    see                 TEXT
);

CREATE TYPE NLP_TASK AS ENUM ('summarization', 'question-answering',
                              'text-classification', 'conversational',
                              'translation');
CREATE TABLE model (
    model_id            SERIAL PRIMARY KEY,
    name                TEXT UNIQUE NOT NULL,
    family_name         TEXT NOT NULL
        CONSTRAINT FK_family_name
        REFERENCES model_family(name) ON UPDATE CASCADE,
    tasks               NLP_TASK[] NOT NULL,
    vendor_name         TEXT NOT NULL 
        CONSTRAINT FK_vendor_name
        REFERENCES vendor(name) ON UPDATE CASCADE,
    year                DATE,
    see                 TEXT
);

CREATE TYPE STATUS AS ENUM ('preprocessing', 'encoding', 'summarizing',
                            'postprocessing', 'completed');
CREATE TABLE summary (
    summary_id          SERIAL PRIMARY KEY,
    source_id           INTEGER NOT NULL
        CONSTRAINT FK_source_id
        REFERENCES source ON DELETE CASCADE ON UPDATE CASCADE,
    summary             TEXT NOT NULL,
    summary_length      INTEGER NOT NULL CHECK (summary_length > 0),
    model_name          TEXT NOT NULL
        CONSTRAINT FK_model_name
        REFERENCES model(name) ON UPDATE CASCADE,
    params              JSON NOT NULL,
    status              STATUS NOT NULL,
    start_time          TIMESTAMPTZ NOT NULL,
    end_time            TIMESTAMPTZ,
    language_tag        TEXT NOT NULL
        CONSTRAINT FK_language_tag
        REFERENCES language(language_tag) ON UPDATE CASCADE
);

/*
* INSERTS
*/
INSERT INTO language
VALUES (DEFAULT, 'English', 'en');

INSERT INTO vendor
VALUES (DEFAULT, 'Hugging Face', 'https://huggingface.co/');

INSERT INTO model_family
VALUES (DEFAULT, 'T5', '{ "Colin Raffel","Noam Shazeer", "Adam Roberts",
                 "Katherine Lee", "Sharan Narang", "Michael Matena",
                 "Yanqi Zhou", "Wei Li", "Peter J. Liu"}',
        '{"Google"}', '2019-10-23', 'https://arxiv.org/abs/1910.10683');

INSERT INTO model
VALUES (DEFAULT, 't5-large', 'T5', '{"summarization", "translation"}',
        'Hugging Face', '2019-12-12',
        'https://huggingface.co/transformers/model_doc/t5.html');
