# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5314
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class ForwardRateAgreement(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'start_date': 'datetime',
        'maturity_date': 'datetime',
        'dom_ccy': 'str',
        'fixing_date': 'datetime',
        'fra_rate': 'float',
        'notional': 'float',
        'index_convention': 'IndexConvention',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'maturity_date': 'maturityDate',
        'dom_ccy': 'domCcy',
        'fixing_date': 'fixingDate',
        'fra_rate': 'fraRate',
        'notional': 'notional',
        'index_convention': 'indexConvention',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'maturity_date': 'required',
        'dom_ccy': 'required',
        'fixing_date': 'required',
        'fra_rate': 'required',
        'notional': 'required',
        'index_convention': 'optional',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, maturity_date=None, dom_ccy=None, fixing_date=None, fra_rate=None, notional=None, index_convention=None, instrument_type=None, local_vars_configuration=None):  # noqa: E501
        """ForwardRateAgreement - a model defined in OpenAPI"
        
        :param start_date:  The settlement date of the FRA (required)
        :type start_date: datetime
        :param maturity_date:  The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date. (required)
        :type maturity_date: datetime
        :param dom_ccy:  The domestic currency of the instrument. (required)
        :type dom_ccy: str
        :param fixing_date:  The date at which the rate to be paid, the reference rate, is confirmed/observed. (required)
        :type fixing_date: datetime
        :param fra_rate:  The rate at which the FRA is traded. (required)
        :type fra_rate: float
        :param notional:  The amount for which the FRA is traded. (required)
        :type notional: float
        :param index_convention: 
        :type index_convention: lusid.IndexConvention
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap (required)
        :type instrument_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._start_date = None
        self._maturity_date = None
        self._dom_ccy = None
        self._fixing_date = None
        self._fra_rate = None
        self._notional = None
        self._index_convention = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.maturity_date = maturity_date
        self.dom_ccy = dom_ccy
        self.fixing_date = fixing_date
        self.fra_rate = fra_rate
        self.notional = notional
        if index_convention is not None:
            self.index_convention = index_convention
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this ForwardRateAgreement.  # noqa: E501

        The settlement date of the FRA  # noqa: E501

        :return: The start_date of this ForwardRateAgreement.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this ForwardRateAgreement.

        The settlement date of the FRA  # noqa: E501

        :param start_date: The start_date of this ForwardRateAgreement.  # noqa: E501
        :type start_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_date is None:  # noqa: E501
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def maturity_date(self):
        """Gets the maturity_date of this ForwardRateAgreement.  # noqa: E501

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date.  # noqa: E501

        :return: The maturity_date of this ForwardRateAgreement.  # noqa: E501
        :rtype: datetime
        """
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self, maturity_date):
        """Sets the maturity_date of this ForwardRateAgreement.

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date.  # noqa: E501

        :param maturity_date: The maturity_date of this ForwardRateAgreement.  # noqa: E501
        :type maturity_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and maturity_date is None:  # noqa: E501
            raise ValueError("Invalid value for `maturity_date`, must not be `None`")  # noqa: E501

        self._maturity_date = maturity_date

    @property
    def dom_ccy(self):
        """Gets the dom_ccy of this ForwardRateAgreement.  # noqa: E501

        The domestic currency of the instrument.  # noqa: E501

        :return: The dom_ccy of this ForwardRateAgreement.  # noqa: E501
        :rtype: str
        """
        return self._dom_ccy

    @dom_ccy.setter
    def dom_ccy(self, dom_ccy):
        """Sets the dom_ccy of this ForwardRateAgreement.

        The domestic currency of the instrument.  # noqa: E501

        :param dom_ccy: The dom_ccy of this ForwardRateAgreement.  # noqa: E501
        :type dom_ccy: str
        """
        if self.local_vars_configuration.client_side_validation and dom_ccy is None:  # noqa: E501
            raise ValueError("Invalid value for `dom_ccy`, must not be `None`")  # noqa: E501

        self._dom_ccy = dom_ccy

    @property
    def fixing_date(self):
        """Gets the fixing_date of this ForwardRateAgreement.  # noqa: E501

        The date at which the rate to be paid, the reference rate, is confirmed/observed.  # noqa: E501

        :return: The fixing_date of this ForwardRateAgreement.  # noqa: E501
        :rtype: datetime
        """
        return self._fixing_date

    @fixing_date.setter
    def fixing_date(self, fixing_date):
        """Sets the fixing_date of this ForwardRateAgreement.

        The date at which the rate to be paid, the reference rate, is confirmed/observed.  # noqa: E501

        :param fixing_date: The fixing_date of this ForwardRateAgreement.  # noqa: E501
        :type fixing_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and fixing_date is None:  # noqa: E501
            raise ValueError("Invalid value for `fixing_date`, must not be `None`")  # noqa: E501

        self._fixing_date = fixing_date

    @property
    def fra_rate(self):
        """Gets the fra_rate of this ForwardRateAgreement.  # noqa: E501

        The rate at which the FRA is traded.  # noqa: E501

        :return: The fra_rate of this ForwardRateAgreement.  # noqa: E501
        :rtype: float
        """
        return self._fra_rate

    @fra_rate.setter
    def fra_rate(self, fra_rate):
        """Sets the fra_rate of this ForwardRateAgreement.

        The rate at which the FRA is traded.  # noqa: E501

        :param fra_rate: The fra_rate of this ForwardRateAgreement.  # noqa: E501
        :type fra_rate: float
        """
        if self.local_vars_configuration.client_side_validation and fra_rate is None:  # noqa: E501
            raise ValueError("Invalid value for `fra_rate`, must not be `None`")  # noqa: E501

        self._fra_rate = fra_rate

    @property
    def notional(self):
        """Gets the notional of this ForwardRateAgreement.  # noqa: E501

        The amount for which the FRA is traded.  # noqa: E501

        :return: The notional of this ForwardRateAgreement.  # noqa: E501
        :rtype: float
        """
        return self._notional

    @notional.setter
    def notional(self, notional):
        """Sets the notional of this ForwardRateAgreement.

        The amount for which the FRA is traded.  # noqa: E501

        :param notional: The notional of this ForwardRateAgreement.  # noqa: E501
        :type notional: float
        """
        if self.local_vars_configuration.client_side_validation and notional is None:  # noqa: E501
            raise ValueError("Invalid value for `notional`, must not be `None`")  # noqa: E501

        self._notional = notional

    @property
    def index_convention(self):
        """Gets the index_convention of this ForwardRateAgreement.  # noqa: E501


        :return: The index_convention of this ForwardRateAgreement.  # noqa: E501
        :rtype: lusid.IndexConvention
        """
        return self._index_convention

    @index_convention.setter
    def index_convention(self, index_convention):
        """Sets the index_convention of this ForwardRateAgreement.


        :param index_convention: The index_convention of this ForwardRateAgreement.  # noqa: E501
        :type index_convention: lusid.IndexConvention
        """

        self._index_convention = index_convention

    @property
    def instrument_type(self):
        """Gets the instrument_type of this ForwardRateAgreement.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :return: The instrument_type of this ForwardRateAgreement.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this ForwardRateAgreement.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :param instrument_type: The instrument_type of this ForwardRateAgreement.  # noqa: E501
        :type instrument_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashFlowsLeg", "Unknown", "TermDeposit", "ContractForDifference", "EquitySwap", "CashPerpetual", "CapFloor", "CashSettled", "CdsIndex", "Basket", "FundingLeg", "FxSwap", "ForwardRateAgreement", "SimpleInstrument", "Repo", "Equity", "ExchangeTradedOption", "ReferenceInstrument", "ComplexBond", "InflationLinkedBond", "InflationSwap"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ForwardRateAgreement):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ForwardRateAgreement):
            return True

        return self.to_dict() != other.to_dict()
