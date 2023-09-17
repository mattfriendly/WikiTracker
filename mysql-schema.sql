CREATE TABLE `shipments` (
  `id` INT(11) NOT NULL,
  `shipper_name` VARCHAR(255) DEFAULT NULL,
  `shipper_phone` VARCHAR(255) DEFAULT NULL,
  `shipper_company` VARCHAR(255) DEFAULT NULL,
  `shipper_street` VARCHAR(255) DEFAULT NULL,
  `shipper_city` VARCHAR(255) DEFAULT NULL,
  `shipper_state` VARCHAR(255) DEFAULT NULL,
  `shipper_postal` VARCHAR(255) DEFAULT NULL,
  `shipper_country` VARCHAR(255) DEFAULT NULL,
  `recipient_name` VARCHAR(255) DEFAULT NULL,
  `recipient_phone` VARCHAR(255) DEFAULT NULL,
  `recipient_company` VARCHAR(255) DEFAULT NULL,
  `recipient_street1` VARCHAR(255) DEFAULT NULL,
  `recipient_street2` VARCHAR(255) DEFAULT NULL,
  `recipient_city` VARCHAR(255) DEFAULT NULL,
  `recipient_state` VARCHAR(255) DEFAULT NULL,
  `recipient_postal` VARCHAR(255) DEFAULT NULL,
  `recipient_country` VARCHAR(255) DEFAULT NULL,
  `ship_datestamp` VARCHAR(255) DEFAULT NULL,
  `service_type` VARCHAR(255) DEFAULT NULL,
  `packaging_type` VARCHAR(255) DEFAULT NULL,
  `pickup_type` VARCHAR(255) DEFAULT NULL,
  `block_insight_visibility` VARCHAR(255) DEFAULT NULL,
  `payment_type` VARCHAR(255) DEFAULT NULL,
  `image_type` VARCHAR(255) DEFAULT NULL,
  `label_stock_type` VARCHAR(255) DEFAULT NULL,
  `weight_value` TINYINT(10) DEFAULT NULL,
  `weight_units` VARCHAR(255) DEFAULT NULL,
  `account_number` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_street1` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_street2` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_city` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_state` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_postal` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_country` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_residential` BOOLEAN DEFAULT NULL,
  `shipping_charges_person_name` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_email` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_phone` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_phone_extension` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_company_name` VARCHAR(255) DEFAULT NULL,
  `shipping_charges_fax_number` VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;