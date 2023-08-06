"""
main_interactors.py

this file contains the main interactors of this monad.
an interactor is a function that responds to business commands and
business events.

typically UI applications (or CLI) invokes commands.
the monad responds to the commands by performing business logic.
the monad returns a response to the caller.
the monad could emit business events.
finally, monad could respond to business events.

monad is a fundamental unit of business functionality.
monad is self-sufficient and contains all the necessary "brains" to perform the business functionality.
monad has all the intelligence to bring microservice to life.
just add an infrastructure to monad and you get microservice.

monad should never invoke another monad's command (anti-pattern)

"""
import aa.business_logic.report_status
import aa.business_logic.report_generator
import aa.business_logic.authenticator
import aa.business_logic.authorizer
from aa.business_logic.report_validator import is_date_valid
from aa.plug_point_config import monad_aa_plug_point_configuration
from plugin.plugin_manager import PluginManager


def initiate_report_generation(authentication_identifier, account_nbr, date):
    # system checks if user is authenticated
    # calls a plug point.
    user_id, authenticated = aa.business_logic.authenticator.authenticate_user(
        authentication_identifier,  # this identifies the user. in FTD it is session cookie FTD_AUTH
    )
    #   if authenticated is True user_id is set to a valid user
    #   if authenticated is False user_id is set to None
    if not authenticated:
        raise ValueError("user_not_authenticated")

    # system checks if user has appropriate entitlements
    # calls a plug point.
    authenticated = aa.business_logic.authorizer.is_user_entitled_to_account(
        authentication_identifier,  # this identifies the user. in FTD it is session cookie FTD_AUTH
        user_id,
        account_nbr
    )

    is_date_valid(date)

    report_id = aa.business_logic.report_generator.generate_unique_report_id()

    aa.business_logic.report_status.save_as(report_id, "INITIATED")

    # TODO kick off queue plug-point here
    aa.business_logic.report_generator.generate_now(report_id, account_nbr, date)

    return report_id


def is_report_ready(authentication_identifier, report_id):
    return False

