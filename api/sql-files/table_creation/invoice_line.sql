CREATE TABLE IF NOT EXISTS INVOICE_LINE (
	INVT_CODE INTEGER UNSIGNED,
    INV_ID INTEGER UNSIGNED,
    QTY SMALLINT NOT NULL,
    UNIT_PRICE DECIMAL(6, 2) NOT NULL,
    PRIMARY KEY (INVT_CODE, INV_ID),
    FOREIGN KEY (INVT_CODE) REFERENCES INVENTORY (INVT_CODE) ON DELETE CASCADE,
    FOREIGN KEY (INV_ID) REFERENCES INVOICE (INV_ID) ON DELETE CASCADE
);

