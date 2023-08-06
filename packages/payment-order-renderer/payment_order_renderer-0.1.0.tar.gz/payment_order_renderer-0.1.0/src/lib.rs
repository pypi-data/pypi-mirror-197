use pyo3::{prelude::*};
use chrono::prelude::{NaiveDate, NaiveDateTime};

mod pdf_builder;
use pdf_builder::create_payment_report;


#[pyclass]
pub struct PaymentOrder {
    #[pyo3(get, set)]
    creation_date: String,
    #[pyo3(get, set)]
    last_transaction_date: String,
    #[pyo3(get, set)]
    document_date: String,
    #[pyo3(get, set)]
    document_number: String,
    #[pyo3(get, set)]
    priority: String,
    #[pyo3(get, set)]
    transaction_type_code: String,
    #[pyo3(get, set)]
    purpose: String,

    #[pyo3(get, set)]
    payer_kpp: String,
    #[pyo3(get, set)]
    payer_inn: String,
    #[pyo3(get, set)]
    payer_name: String,
    #[pyo3(get, set)]
    payer_bank: String,
    #[pyo3(get, set)]
    payer_bank_address: String,

    #[pyo3(get, set)]
    side_recipient_inn: String,
    #[pyo3(get, set)]
    side_recipient_bank: String,
    #[pyo3(get, set)]
    side_recipient_bank_address: String,
    #[pyo3(get, set)]
    side_recipient_name: String,
    #[pyo3(get, set)]
    side_recipient_kpp: Option<String>,

    #[pyo3(get, set)]
    transaction_sum: String,
    #[pyo3(get, set)]
    payer_account: String,
    #[pyo3(get, set)]
    payer_bank_code: String,
    #[pyo3(get, set)]
    payer_cr_account: String,

    #[pyo3(get, set)]
    side_recipient_bank_code: String,
    #[pyo3(get, set)]
    side_recipient_account: String,
    #[pyo3(get, set)]
    side_recipient_cr_account: String,
    finance_administrator_name: String,
}


#[pymethods]
impl PaymentOrder {
    #[new] 
    #[pyo3(signature = (
        creation_date,
        last_transaction_date,
        document_date,
        document_number,
        priority,
        transaction_type_code,
        purpose,
        payer_kpp,
        payer_inn,
        payer_name,
        payer_bank,
        payer_bank_address,
        side_recipient_inn,
        side_recipient_bank,
        side_recipient_bank_address,
        side_recipient_name,
        side_recipient_kpp,
        transaction_sum,
        payer_account,
        payer_bank_code,
        payer_cr_account,
        side_recipient_bank_code,
        side_recipient_account,
        side_recipient_cr_account,
        finance_administrator_name,
    ))]
    fn new(
        creation_date: String,
        last_transaction_date: String,
        document_date: String,
        document_number: String,
        priority: String,
        transaction_type_code: String,
        purpose: String,

        payer_kpp: String,
        payer_inn: String,
        payer_name: String,
        payer_bank: String,
        payer_bank_address: String,

        side_recipient_inn: String,
        side_recipient_bank: String,
        side_recipient_bank_address: String,
        side_recipient_name: String,
        side_recipient_kpp: Option<String>,

        transaction_sum: String,
        payer_account: String,
        payer_bank_code: String,
        payer_cr_account: String,

        side_recipient_bank_code: String,
        side_recipient_account: String,
        side_recipient_cr_account: String,
        finance_administrator_name: String,
    ) -> Self {
        PaymentOrder {
            creation_date,
            last_transaction_date,
            document_date,
            document_number,
            priority,
            transaction_type_code,
            purpose,
            payer_kpp,
            payer_inn,
            payer_name,
            payer_bank,
            payer_bank_address,

            side_recipient_inn,
            side_recipient_bank,
            side_recipient_bank_address,
            side_recipient_name,
            side_recipient_kpp,

            transaction_sum,
            payer_account,
            payer_bank_code,
            payer_cr_account,

            side_recipient_bank_code,
            side_recipient_account,
            side_recipient_cr_account,
            finance_administrator_name,
        }
    }
}


impl PaymentOrder {
    fn reform_payment_ending(&mut self) {
        /*  Если число без остатка, то нужно возращать его  виде "12=",
            Если с остатком, то в виде "12-11"
        */
        let payment_integer = match self.transaction_sum.parse::<f64>() {
            Ok(payment) if payment == payment.trunc() || self.transaction_sum.ends_with(".00") => {
                format!("{}=", payment as i64)
            },
            Ok(payment) => {
                let payment_integer_part = payment.trunc() as i64;
                let payment_decimal_part = (payment.fract() * 100.0) as i64;
                format!("{}-{:02}", payment_integer_part, payment_decimal_part)
            },
            Err(_) => self.transaction_sum.clone(),
        };
        self.transaction_sum = payment_integer;
    }
}


impl PaymentOrder {
    fn validate_dates(&mut self) {
        /*  Приводим даты из вида "2023-02-21" и "2023-02-21T09:39:47.177000+00:00" 
        к виду "21-02-2023" 
        */
        let mut dates = [
            &mut self.creation_date,
            &mut self.last_transaction_date,
            &mut self.document_date,
        ];
        
        for date in dates.iter_mut() {
            let parsed_date = match NaiveDateTime::parse_from_str(date, "%Y-%m-%dT%H:%M:%S%.f%z") {
                Ok(dt) => dt.date(),
                Err(_) => match NaiveDate::parse_from_str(date, "%Y-%m-%d") {
                    Ok(d) => d,
                    Err(_) => panic!("Некорректный формат даты: {}", date),
                },
            };
            **date = parsed_date.format("%d.%m.%Y").to_string();
        }
    }
}


#[pyfunction]
fn create_pdf(py: Python, payment_order: &mut PaymentOrder, path: &str) -> PyResult<Vec<u8>> {
    payment_order.reform_payment_ending();
    payment_order.validate_dates();
    
    let bytes = create_payment_report(payment_order, path);
    Ok(bytes.unwrap())
}


/// A Python module implemented in Rust.
#[pymodule]
fn payment_order_renderer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PaymentOrder>()?;
    m.add_function(wrap_pyfunction!(create_pdf, m)?)?;
    Ok(())
}