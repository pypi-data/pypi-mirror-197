import aa


def generate_unique_report_id():
    # TODO generate a uuid
    return 12345


def retrieve_aa_data(account_number, date):
    return {"this": "that"}


def save_aa_report(file):
    pass


def generate_now(report_id, account_number, date):
    # retrieve data from the backend
    # this is through a plug-point
    aa_data = retrieve_aa_data(account_number, date)

    # apply any business logic to transform the data
    # or filter or do stuff to make the data usable
    # copy data into a file
    file = "report contents go here"

    # save file
    save_aa_report(file)

    aa.business_logic.report_status.save_as(report_id, "COMPLETED")
