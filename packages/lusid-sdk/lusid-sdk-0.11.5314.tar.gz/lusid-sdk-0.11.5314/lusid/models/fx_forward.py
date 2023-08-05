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


class FxForward(object):
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
        'dom_amount': 'float',
        'dom_ccy': 'str',
        'fgn_amount': 'float',
        'fgn_ccy': 'str',
        'ref_spot_rate': 'float',
        'is_ndf': 'bool',
        'fixing_date': 'datetime',
        'settlement_ccy': 'str',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'maturity_date': 'maturityDate',
        'dom_amount': 'domAmount',
        'dom_ccy': 'domCcy',
        'fgn_amount': 'fgnAmount',
        'fgn_ccy': 'fgnCcy',
        'ref_spot_rate': 'refSpotRate',
        'is_ndf': 'isNdf',
        'fixing_date': 'fixingDate',
        'settlement_ccy': 'settlementCcy',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'maturity_date': 'required',
        'dom_amount': 'required',
        'dom_ccy': 'required',
        'fgn_amount': 'required',
        'fgn_ccy': 'required',
        'ref_spot_rate': 'optional',
        'is_ndf': 'optional',
        'fixing_date': 'optional',
        'settlement_ccy': 'optional',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, maturity_date=None, dom_amount=None, dom_ccy=None, fgn_amount=None, fgn_ccy=None, ref_spot_rate=None, is_ndf=None, fixing_date=None, settlement_ccy=None, instrument_type=None, local_vars_configuration=None):  # noqa: E501
        """FxForward - a model defined in OpenAPI"
        
        :param start_date:  The start date of the instrument. This is normally synonymous with the trade-date. (required)
        :type start_date: datetime
        :param maturity_date:  The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it. (required)
        :type maturity_date: datetime
        :param dom_amount:  The amount that is to be paid in the domestic currency on the maturity date. (required)
        :type dom_amount: float
        :param dom_ccy:  The domestic currency of the instrument. (required)
        :type dom_ccy: str
        :param fgn_amount:  The amount that is to be paid in the foreign currency on the maturity date. (required)
        :type fgn_amount: float
        :param fgn_ccy:  The foreign (other) currency of the instrument. In the NDF case, only payments are made in the domestic currency.  For the outright forward, currencies are exchanged. By domestic is then that of the portfolio. (required)
        :type fgn_ccy: str
        :param ref_spot_rate:  The reference Fx Spot rate for currency pair Foreign-Domestic that was seen on the trade start date (time).
        :type ref_spot_rate: float
        :param is_ndf:  Is the contract an Fx-Forward of \"Non-Deliverable\" type, meaning a single payment in the domestic currency based on the change in fx-rate vs  a reference rate is used.
        :type is_ndf: bool
        :param fixing_date:  The fixing date.
        :type fixing_date: datetime
        :param settlement_ccy:  The settlement currency.  If provided, present value will be calculated in settlement currency, otherwise the domestic currency. Applies only to non-deliverable FX Forwards.
        :type settlement_ccy: str
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap (required)
        :type instrument_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._start_date = None
        self._maturity_date = None
        self._dom_amount = None
        self._dom_ccy = None
        self._fgn_amount = None
        self._fgn_ccy = None
        self._ref_spot_rate = None
        self._is_ndf = None
        self._fixing_date = None
        self._settlement_ccy = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.maturity_date = maturity_date
        self.dom_amount = dom_amount
        self.dom_ccy = dom_ccy
        self.fgn_amount = fgn_amount
        self.fgn_ccy = fgn_ccy
        if ref_spot_rate is not None:
            self.ref_spot_rate = ref_spot_rate
        if is_ndf is not None:
            self.is_ndf = is_ndf
        if fixing_date is not None:
            self.fixing_date = fixing_date
        self.settlement_ccy = settlement_ccy
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this FxForward.  # noqa: E501

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :return: The start_date of this FxForward.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this FxForward.

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :param start_date: The start_date of this FxForward.  # noqa: E501
        :type start_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_date is None:  # noqa: E501
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def maturity_date(self):
        """Gets the maturity_date of this FxForward.  # noqa: E501

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it.  # noqa: E501

        :return: The maturity_date of this FxForward.  # noqa: E501
        :rtype: datetime
        """
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self, maturity_date):
        """Sets the maturity_date of this FxForward.

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it.  # noqa: E501

        :param maturity_date: The maturity_date of this FxForward.  # noqa: E501
        :type maturity_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and maturity_date is None:  # noqa: E501
            raise ValueError("Invalid value for `maturity_date`, must not be `None`")  # noqa: E501

        self._maturity_date = maturity_date

    @property
    def dom_amount(self):
        """Gets the dom_amount of this FxForward.  # noqa: E501

        The amount that is to be paid in the domestic currency on the maturity date.  # noqa: E501

        :return: The dom_amount of this FxForward.  # noqa: E501
        :rtype: float
        """
        return self._dom_amount

    @dom_amount.setter
    def dom_amount(self, dom_amount):
        """Sets the dom_amount of this FxForward.

        The amount that is to be paid in the domestic currency on the maturity date.  # noqa: E501

        :param dom_amount: The dom_amount of this FxForward.  # noqa: E501
        :type dom_amount: float
        """
        if self.local_vars_configuration.client_side_validation and dom_amount is None:  # noqa: E501
            raise ValueError("Invalid value for `dom_amount`, must not be `None`")  # noqa: E501

        self._dom_amount = dom_amount

    @property
    def dom_ccy(self):
        """Gets the dom_ccy of this FxForward.  # noqa: E501

        The domestic currency of the instrument.  # noqa: E501

        :return: The dom_ccy of this FxForward.  # noqa: E501
        :rtype: str
        """
        return self._dom_ccy

    @dom_ccy.setter
    def dom_ccy(self, dom_ccy):
        """Sets the dom_ccy of this FxForward.

        The domestic currency of the instrument.  # noqa: E501

        :param dom_ccy: The dom_ccy of this FxForward.  # noqa: E501
        :type dom_ccy: str
        """
        if self.local_vars_configuration.client_side_validation and dom_ccy is None:  # noqa: E501
            raise ValueError("Invalid value for `dom_ccy`, must not be `None`")  # noqa: E501

        self._dom_ccy = dom_ccy

    @property
    def fgn_amount(self):
        """Gets the fgn_amount of this FxForward.  # noqa: E501

        The amount that is to be paid in the foreign currency on the maturity date.  # noqa: E501

        :return: The fgn_amount of this FxForward.  # noqa: E501
        :rtype: float
        """
        return self._fgn_amount

    @fgn_amount.setter
    def fgn_amount(self, fgn_amount):
        """Sets the fgn_amount of this FxForward.

        The amount that is to be paid in the foreign currency on the maturity date.  # noqa: E501

        :param fgn_amount: The fgn_amount of this FxForward.  # noqa: E501
        :type fgn_amount: float
        """
        if self.local_vars_configuration.client_side_validation and fgn_amount is None:  # noqa: E501
            raise ValueError("Invalid value for `fgn_amount`, must not be `None`")  # noqa: E501

        self._fgn_amount = fgn_amount

    @property
    def fgn_ccy(self):
        """Gets the fgn_ccy of this FxForward.  # noqa: E501

        The foreign (other) currency of the instrument. In the NDF case, only payments are made in the domestic currency.  For the outright forward, currencies are exchanged. By domestic is then that of the portfolio.  # noqa: E501

        :return: The fgn_ccy of this FxForward.  # noqa: E501
        :rtype: str
        """
        return self._fgn_ccy

    @fgn_ccy.setter
    def fgn_ccy(self, fgn_ccy):
        """Sets the fgn_ccy of this FxForward.

        The foreign (other) currency of the instrument. In the NDF case, only payments are made in the domestic currency.  For the outright forward, currencies are exchanged. By domestic is then that of the portfolio.  # noqa: E501

        :param fgn_ccy: The fgn_ccy of this FxForward.  # noqa: E501
        :type fgn_ccy: str
        """
        if self.local_vars_configuration.client_side_validation and fgn_ccy is None:  # noqa: E501
            raise ValueError("Invalid value for `fgn_ccy`, must not be `None`")  # noqa: E501

        self._fgn_ccy = fgn_ccy

    @property
    def ref_spot_rate(self):
        """Gets the ref_spot_rate of this FxForward.  # noqa: E501

        The reference Fx Spot rate for currency pair Foreign-Domestic that was seen on the trade start date (time).  # noqa: E501

        :return: The ref_spot_rate of this FxForward.  # noqa: E501
        :rtype: float
        """
        return self._ref_spot_rate

    @ref_spot_rate.setter
    def ref_spot_rate(self, ref_spot_rate):
        """Sets the ref_spot_rate of this FxForward.

        The reference Fx Spot rate for currency pair Foreign-Domestic that was seen on the trade start date (time).  # noqa: E501

        :param ref_spot_rate: The ref_spot_rate of this FxForward.  # noqa: E501
        :type ref_spot_rate: float
        """

        self._ref_spot_rate = ref_spot_rate

    @property
    def is_ndf(self):
        """Gets the is_ndf of this FxForward.  # noqa: E501

        Is the contract an Fx-Forward of \"Non-Deliverable\" type, meaning a single payment in the domestic currency based on the change in fx-rate vs  a reference rate is used.  # noqa: E501

        :return: The is_ndf of this FxForward.  # noqa: E501
        :rtype: bool
        """
        return self._is_ndf

    @is_ndf.setter
    def is_ndf(self, is_ndf):
        """Sets the is_ndf of this FxForward.

        Is the contract an Fx-Forward of \"Non-Deliverable\" type, meaning a single payment in the domestic currency based on the change in fx-rate vs  a reference rate is used.  # noqa: E501

        :param is_ndf: The is_ndf of this FxForward.  # noqa: E501
        :type is_ndf: bool
        """

        self._is_ndf = is_ndf

    @property
    def fixing_date(self):
        """Gets the fixing_date of this FxForward.  # noqa: E501

        The fixing date.  # noqa: E501

        :return: The fixing_date of this FxForward.  # noqa: E501
        :rtype: datetime
        """
        return self._fixing_date

    @fixing_date.setter
    def fixing_date(self, fixing_date):
        """Sets the fixing_date of this FxForward.

        The fixing date.  # noqa: E501

        :param fixing_date: The fixing_date of this FxForward.  # noqa: E501
        :type fixing_date: datetime
        """

        self._fixing_date = fixing_date

    @property
    def settlement_ccy(self):
        """Gets the settlement_ccy of this FxForward.  # noqa: E501

        The settlement currency.  If provided, present value will be calculated in settlement currency, otherwise the domestic currency. Applies only to non-deliverable FX Forwards.  # noqa: E501

        :return: The settlement_ccy of this FxForward.  # noqa: E501
        :rtype: str
        """
        return self._settlement_ccy

    @settlement_ccy.setter
    def settlement_ccy(self, settlement_ccy):
        """Sets the settlement_ccy of this FxForward.

        The settlement currency.  If provided, present value will be calculated in settlement currency, otherwise the domestic currency. Applies only to non-deliverable FX Forwards.  # noqa: E501

        :param settlement_ccy: The settlement_ccy of this FxForward.  # noqa: E501
        :type settlement_ccy: str
        """

        self._settlement_ccy = settlement_ccy

    @property
    def instrument_type(self):
        """Gets the instrument_type of this FxForward.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :return: The instrument_type of this FxForward.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this FxForward.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap  # noqa: E501

        :param instrument_type: The instrument_type of this FxForward.  # noqa: E501
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
        if not isinstance(other, FxForward):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FxForward):
            return True

        return self.to_dict() != other.to_dict()
