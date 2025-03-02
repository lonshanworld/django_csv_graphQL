# schema.py
import csv
import io
import graphene
from graphene_file_upload.scalars import Upload

# Define a GraphQL type for the challenge data
class ChallengeType(graphene.ObjectType):
    challenge_id = graphene.Int()
    challenge_name = graphene.String()
    challenge_success_rate = graphene.Int()

# Define a mutation for uploading and processing the CSV file
class UploadCSV(graphene.Mutation):
    class Arguments:
        # 'file' is required and uses the Upload scalar
        file = Upload(required=True)

    # Define the fields returned by the mutation
    challenges = graphene.List(ChallengeType)
    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # Read and decode the CSV file (assuming UTF-8)
        try:
            decoded_file = file.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error decoding file: {e}")

        # Use StringIO to treat the decoded string as a file-like object
        csv_data = io.StringIO(decoded_file)
        reader = csv.DictReader(csv_data)

        challenges_list = []
        for row in reader:
            try:
                # Convert and extract values from the CSV row
                challenge_id = int(row.get('ChallengeID', 0))
                challenge_name = row.get('ChallengeName', '')
                challenge_success_rate = int(row.get('ChallengeSucessRate', 0))
            except Exception as e:
                continue  # Skip rows with issues

            challenges_list.append(
                ChallengeType(
                    challenge_id=challenge_id,
                    challenge_name=challenge_name,
                    challenge_success_rate=challenge_success_rate,
                )
            )

        return UploadCSV(challenges=challenges_list, success=True)

# Define the root mutation
class Mutation(graphene.ObjectType):
    upload_csv = UploadCSV.Field()

# Optionally, define a Query type if you want to add queries later
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

# Create the schema with Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
