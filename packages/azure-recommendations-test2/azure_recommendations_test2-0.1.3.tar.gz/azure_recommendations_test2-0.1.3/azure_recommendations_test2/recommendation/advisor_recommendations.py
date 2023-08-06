import logging

from azure.identity import ClientSecretCredential
from azure.mgmt.advisor import AdvisorManagementClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class advisor_recommendations:
    def __init__(self, credentials: ClientSecretCredential, authorization_token: str):
        """
        :param credentials: ClientSecretCredential
        """
        self.credentials = credentials
        self.authorization_token = authorization_token

    # Provides the recommendation from Azure advisor
    def azure_advisor_recommendations(self, subscription_list: list) -> list:
        """
        :param subscription_list: list of azure subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside advisor_recommendations :: azure_advisor_recommendations()--- ")

        response = []

        for subscription in subscription_list:
            advisor_client = AdvisorManagementClient(credential=self.credentials, subscription_id=subscription)

            recommendation_list = advisor_client.recommendations.list()
            for recommendation in recommendation_list:
                temp = {
                    'recommendation': recommendation.short_description.solution,
                    'description': recommendation.short_description.solution,
                    'resource': recommendation.resource_metadata.resource_id.split('/')[-2],
                    'subscription_id': subscription,
                    'resource_id': recommendation.resource_metadata.resource_id,
                    'metadata': {},
                    'current cost': 0,
                    'effective cost': 0,
                    'savings': 0,
                    'savings %': 0

                }
                response.append(temp)
                # print(recommendation.category)
                # print(recommendation.short_description.solution)
                # print(recommendation.resource_metadata)

        return response
