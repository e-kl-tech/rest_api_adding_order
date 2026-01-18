-- Получение информации о сумме товаров заказанных под каждого клиента (Наименование клиента, сумма)
SELECT 
    c.Name AS "Клиент", 
    SUM(oi.Total_Price) AS "Сумма"
FROM 
    CLIENTS c
JOIN 
    ORDERS o ON c.ID = o.Customer_ID
JOIN 
    ORDER_ITEMS oi ON o.ID = oi.Order_ID
GROUP BY 
    c.Name;
	
-- Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры
SELECT 
    p.Name AS "Наименование категории", 
    COUNT(c.ID) AS "Количество дочерних элементов"
FROM 
    CATEGORIES p
LEFT JOIN 
    CATEGORIES c ON p.ID = c.Parent_ID
GROUP BY 
    p.ID, p.Name;
	
-- Написать текст запроса для отчета (view) «Топ-5 самых покупаемых товаров за последний месяц» (по количеству штук в заказах). В отчете должны быть: Наименование товара, Категория 1-го уровня, Общее количество проданных штук.
CREATE OR REPLACE VIEW top_5_products_last_month AS
WITH RECURSIVE category_path AS (
    SELECT 
        id, 
        name, 
        parent_id, 
        id as level_1_id,
        name as level_1_name
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL
    
    SELECT 
        c.id, 
        c.name, 
        c.parent_id, 
        cp.level_1_id, 
        cp.level_1_name
    FROM categories c
    JOIN category_path cp ON c.parent_id = cp.id
)
SELECT 
    p.Name AS "Наименование товара",
    cp.level_1_name AS "Категория 1-го уровня",
    SUM(oi.Quantity) AS "Общее количество проданных штук"
FROM 
    ORDER_ITEMS oi
JOIN 
    ORDERS o ON oi.Order_ID = o.ID
JOIN 
    PRODUCTS p ON oi.Product_ID = p.ID
JOIN 
    category_path cp ON p.Category_ID = cp.id
WHERE 
    o.Order_Date >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY 
    p.ID, p.Name, cp.level_1_name
ORDER BY 
    "Общее количество проданных штук" DESC
LIMIT 5;