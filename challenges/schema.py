import csv
import io
import graphene
from graphene_file_upload.scalars import Upload

class ChallengeType(graphene.ObjectType):
    challenge_id = graphene.Int()
    challenge_name = graphene.String()
    challenge_success_rate = graphene.Int()

class UploadCSV(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    challenges = graphene.List(ChallengeType)
    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        try:
            decoded_file = file.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error decoding file: {e}")

        csv_data = io.StringIO(decoded_file)
        reader = csv.DictReader(csv_data)

        challenges_list = []
        for row in reader:
            try:
                challenge_id = int(row.get('ChallengeID', 0))
                challenge_name = row.get('ChallengeName', '')
                challenge_success_rate = int(row.get('ChallengeSucessRate', 0))
            except Exception as e:
                continue 
            challenges_list.append(
                ChallengeType(
                    challenge_id=challenge_id,
                    challenge_name=challenge_name,
                    challenge_success_rate=challenge_success_rate,
                )
            )

        return UploadCSV(challenges=challenges_list, success=True)

class Mutation(graphene.ObjectType):
    upload_csv = UploadCSV.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query, mutation=Mutation)
